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
    sendChatMessage(request)
        .then((response) => {
            onMessage(response.response);
            onComplete();
        })
        .catch((error) => {
            onError(error instanceof Error ? error: new Error(String(error)));
        });

    return () => {
        // TODO: clean up code
    }
}
