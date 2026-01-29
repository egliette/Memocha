'use client';

import Image from 'next/image';
import type { Message } from '@/types/chat';


interface MessageListProps {
    messages: Message[];
    isLoading?: boolean;
}

export default function MessageList({ messages, isLoading }: MessageListProps) {
    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
                <div className="text-center text-gray-400 mt-8">
                    <p>No messages yet. Start a conversation!</p>
                </div>
            ) : (
                messages.filter((message) => !(message.role === 'assistant' && message.content === '')).map((message) => (
                    <div
                        key={message.id}
                        className={`flex items-start gap-3 ${
                            message.role === 'user' ? 'justify-end' : 'justify-start'
                        }`}
                    >
                        {message.role === 'assistant' && (
                            <div className="flex-shrink-0 pt-1">
                                <img
                                    src="/avatar.jpg"
                                    alt="Assistant"
                                    className="w-12 h-12 rounded-full object-cover border-2 border-gray-600"
                                />
                            </div>
                        )}

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
            {/* Loading animation bubble */}
            {isLoading && (
                <div className="flex items-start gap-3">
                    {/* Avatar */}
                    <div className="flex-shrink-0">
                        <Image
                            src="/avatar.jpg"
                            alt="Assistant"
                            width={48}
                            height={48}
                            className="rounded-full border-2 border-gray-600"
                        />
                    </div>
                    {/* Loading bubble */}
                    <div className="max-w-[80%] px-4 py-3 rounded-2xl bg-gray-700">
                        <p className="text-sm font-semibold text-gray-300 mb-1">Assistant</p>
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
}
