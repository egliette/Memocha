'use client';

import type { Message } from '@/types/chat';


interface MessageListProps {
    messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
                <div className="text-center text-gray-400 mt-8">
                    <p>No messages yet. Start a conversation!</p>
                </div>
            ) : (
                messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex ${
                            message.role === 'user' ? 'justify-end' : 'justify-start'
                        }`}
                    >
                        <div
                            className={`max-w-[80%] rounded-lg px-4 py-2 ${
                                message.role === 'user'
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-700 text-gray-100'
                            }`}
                        >
                            <div className="text-sm font-semibold mb-1 opacity-80">
                                {message.role === 'user' ? 'You': 'Assistant'}
                            </div>
                            <div className="whitespace-pre-wrap break-words">
                                {message.content}
                            </div>
                        </div>
                    </div>
               ))
            )}
        </div>
    );
}
