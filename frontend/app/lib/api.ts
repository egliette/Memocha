import axios from 'axios';
import type {
    ChatRequest, ChatResponse, Session, MessageHistoryResponse
} from '@/types/chat';


const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export async function createSession(): Promise<Session> {
    const response = await apiClient.post<Session>('/sessions');
    return response.data;
}

export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/chat', request);
    return response.data;
}

export async function getMessageHistory(
    sessionId: string,
    skip: number = 0,
    limit: number = 100
): Promise<MessageHistoryResponse> {
    const response = await apiClient.get<MessageHistoryResponse>(
        `/sessions/${sessionId}/messages`,
        {
            params: { skip, limit },
        }
    );
    return response.data;
}

// Stream chat response using Server-Sent Events (SSE)
export function streamChatMessage(
    request: ChatRequest,
    onMessage: (chunk: string) => void,
    onError: (error: Error) => void,
    onComplete: () => void
): () => void {
    const abortController = new AbortController();
    let buffer = '';
    let currentEvent = '';
    let currentData = '';

    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

    fetch(`${API_BASE_URL}/chat/stream`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
        signal: abortController.signal,
    })
        .then(async (response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body?.getReader();
            const decoder = new TextDecoder();

            if (!reader) {
                throw new Error('Response body is not readable');
            }

            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    break;
                }

                buffer += decoder.decode(value, { stream: true });

                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (line.startsWith('event:')) {
                        currentEvent = line.substring(6).trim();
                    } else if (line.startsWith('data:')) {
                        currentData = line.substring(5).trim();

                        if (currentData) {
                            try {
                                const parsed = JSON.parse(currentData);

                                if (currentEvent === 'error') {
                                    onError(new Error(parsed.error || parsed.detail || 'Unknown error'));
                                } else if (currentEvent === 'complete') {
                                    onComplete();
                                } else {
                                    if (typeof parsed === 'string') {
                                        onMessage(parsed);
                                    }
                                }
                            } catch (e) {
                                if (!currentEvent || currentEvent === 'message') {
                                    onMessage(currentData);
                                }
                            }
                        }
                    } else if (line === '') {
                        currentEvent = '';
                        currentData = '';
                    }
                }
            }
        })
        .catch((error) => {
            if (error.name === 'AbortError') {
                return;
            }
            onError(error instanceof Error ? error : new Error(String(error)));
        });

    return () => {
        abortController.abort();
    }
}
