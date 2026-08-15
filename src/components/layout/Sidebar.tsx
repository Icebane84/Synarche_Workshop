// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { USER_THEME, useUserContext } from "@core/useUserContext";
import React from "react";
import { NavLink } from "react-router-dom";
import { SystemBiometrics } from "./SystemBiometrics";

interface NavItem {
    name: string;
    path: string;
    icon: React.ReactNode;
}

export const Sidebar: React.FC = () => {
    const { activeUser } = useUserContext();
    const theme = USER_THEME[activeUser];

    const items: NavItem[] = [
        {
            name: "Dashboard",
            path: "/",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                    />
                </svg>
            ),
        },
        {
            name: "Memory Palace",
            path: "/memory",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                </svg>
            ),
        },
        {
            name: "RPG Command",
            path: "/rpg",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222 4 2.222V20"
                    />
                </svg>
            ),
        },
        {
            name: "Knowledge Forge",
            path: "/knowledge",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                    />
                </svg>
            ),
        },
        {
            name: "Chronicle",
            path: "/chronicle",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                </svg>
            ),
        },
        {
            name: "Notifications",
            path: "/notifications",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                    />
                </svg>
            ),
        },
        {
            name: "Tarot Forge",
            path: "/tarot",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L5.595 15.12a2 2 0 00-1.802.735l-.105.132a2 2 0 00-.332 1.705l.775 3.1a2 2 0 001.94 1.515h12.02a2 2 0 001.94-1.515l.775-3.1a2 2 0 00-.332-1.705l-.105-.132zM12 3v9m-4-6l4-4 4 4"
                    />
                </svg>
            ),
        },
        {
            name: "Neo-Genesis",
            path: "/evolution",
            icon: (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L5.595 15.12a2 2 0 00-1.802.735l-.105.132a2 2 0 00-.332 1.705l.775 3.1a2 2 0 001.94 1.515h12.02a2 2 0 001.94-1.515l.775-3.1a2 2 0 00-.332-1.705l-.105-.132zM12 3v9m-4-6l4-4 4 4"
                    />
                </svg>
            ),
        },
    ];

    return (
        <div className="w-[64px] h-full flex flex-col items-center bg-deep-space border-r border-white/5 py-4 select-none">
            {/* HUD Logo */}
            <div className="mb-8 relative flex items-center justify-center">
                <div
                    className="w-10 h-10 border rounded-lg flex items-center justify-center font-mono font-bold text-xs select-none transition-all duration-300"
                    style={{
                        borderColor: theme.accent + "40",
                        color: theme.accent,
                        boxShadow: `0 0 15px ${theme.accent}20`,
                    }}
                >
                    Φ
                </div>
                <div className="absolute -bottom-1 -right-1 w-2.5 h-2.5 bg-green-500 rounded-full border-2 border-deep-space"></div>
            </div>

            {/* Nav items */}
            <nav className="flex-1 w-full flex flex-col items-center gap-4">
                {items.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        title={item.name}
                        className={({ isActive }) =>
                            `relative w-12 h-12 rounded-lg flex items-center justify-center transition-all duration-200 cursor-pointer ${
                                isActive
                                    ? "bg-white/[0.04] text-white"
                                    : "text-white/40 hover:text-white/80 hover:bg-white/[0.02]"
                            }`
                        }
                        style={({ isActive }) =>
                            isActive
                                ? {
                                      border: `1px solid ${theme.accent}30`,
                                      boxShadow: `0 0 10px ${theme.accent}15`,
                                  }
                                : {}
                        }
                    >
                        {({ isActive }) => (
                            <>
                                {item.icon}
                                {isActive && (
                                    <span
                                        className="absolute left-0 top-1/4 bottom-1/4 w-0.5 rounded-r"
                                        style={{ backgroundColor: theme.accent }}
                                    />
                                )}
                            </>
                        )}
                    </NavLink>
                ))}
            </nav>

            {/* Live Biometrics */}
            <SystemBiometrics />

            {/* System Status Label */}
            <div className="text-[9px] font-mono text-white/30 rotate-180 writing-mode-vertical my-4 tracking-[0.15em]">
                PHOENIX v15.0
            </div>
        </div>
    );
};
