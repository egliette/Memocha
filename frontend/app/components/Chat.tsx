'use client';

import { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { createSession, streamChatMessage, getMessageHistory } from '@/lib/api';
import type { Message } from '@/types/chat';

export default function Chat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null >(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        const initSession = async () => {
            try {
                const session = await createSession();
                setSessionId(session.id);

                const history = await getMessageHistory(session.id);
                setMessages(history.messages);
            } catch(err) {
                setError('Failed to initialize session');
                console.error(err);
            }
        };

        initSession();
    }, []);

    const handleSend = async (content: string) => {
        if (!sessionId) {
            setError('Session not initialized');
            return;
        }

        const userMessage: Message = {
            id: `temp-${Date.now()}`,
            role: 'user',
            content,
            created_at: new Date().toISOString(),
            session_id: sessionId,
        };
        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);
        setError(null);

        const tempAssistantId = `temp-${Date.now()}-assistant`;
        const assistantMessage: Message = {
            id: tempAssistantId,
            role: 'assistant',
            content: '',
            created_at: new Date().toISOString(),
            session_id: sessionId,
        };
        setMessages((prev) => [...prev, assistantMessage]);

        const cleanup = streamChatMessage(
            {
                message: content,
                session_id: sessionId,
            },
            (chunk: string) => {
                setMessages((prev) =>
                    prev.map((msg) =>
                        msg.id === tempAssistantId
                            ? {...msg, content: msg.content + chunk }
                            : msg
                    )
                );
            },
            (err: Error) => {
                setError(err.message || 'Failed to send message');
                setMessages((prev) =>
                    prev.filter((msg) => msg.id !== userMessage.id && msg.id !== tempAssistantId)
                );
                setIsLoading(false);
            },
            async () => {
                try {
                    const history = await getMessageHistory(sessionId);
                    setMessages(history.messages);
                } catch (err) {
                    console.error('Failed to fetch message history:', err);
                } finally {
                    setIsLoading(false);
                }
            }
        );
    };

    return (
        <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
            {/* Header */}
            <div className="bg-gray-800 border-b border-gray-700 p-4">
                <h1 className="text-xl font-bold">Memocha Chat</h1>
                {sessionId && (
                    <p className="text-sm text-gray-400">
                        Session: {sessionId.slice(0, 8)}...
                    </p>
                )}
            </div>

            {/* Error banner */}
            {error && (
                <div className="bg-red-900 text-red-100 px-4 py-2 text-sm">
                    Error: {error}
                    <button
                        onClick={() => setError(null)}
                        className="float-right font-bold"
                    >
                        x
                    </button>
                </div>
            )}

            {/* Messages */}
            <div className="flex-1 overflow-auto">
                <MessageList messages={messages} />
                <div ref={messagesEndRef} />
            </div>

            {/* Loading indicator */}
            {isLoading && (
                <div className="px-4 py-2 bg-gray-800 text-gray-400 text-sm">
                    Assistant is typing...
                </div>
            )}

            {/* Input */}
            <MessageInput onSend={handleSend} disabled={isLoading} />
        </div>
    );
}
