'use client';

import { useState, KeyboardEvent } from 'react';

interface MessageInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export default function MessageInput({ onSend, disabled = false }: MessageInputProps) {
    const [message, setMessage] = useState('');

    const handleSend = () => {
        if (message.trim() && !disabled) {
            onSend(message.trim());
            setMessage('');
        }
    };

    const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    }

    return (
        <div className="border-t border-gray-700 p-4 bg-gray-800">
            <div className="flex gap-2">
                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
                    disabled={disabled}
                    className="flex-1 bg-gray-700 text-gray-100 rounded-lg px-4 py-2
                    resize-none focus:outline-none focus: ring-2 focus:ring-blue-500 disabled:opacity-50"
                    rows={1}
                    style={{
                        minHeight: '44px',
                        maxHeight: '120px',
                    }}
                />
                <button
                    onClick={handleSend}
                    disabled={disabled || !message.trim()}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed
                    text-white px-6 py-2 rounded-lg font-medium transition-colors"
                >
                    Send
                </button>
            </div>
        </div>
    );
}
