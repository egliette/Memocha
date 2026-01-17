export interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    created_at: string;
    session_id: string;
}

export interface Session {
    id: string;
    created_at: string;
}

export interface ChatRequest {
    message: string;
    session_id?: string;
}

export interface ChatResponse {
    response: string;
    session_id: string;
}

export interface MessageHistoryResponse {
    messages: Message[];
    session_id: string;
    total: number;
    skip: number;
    limit: number;
}
