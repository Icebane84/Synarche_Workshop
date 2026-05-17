import { useState, useEffect } from 'react';
import type { ReactElement } from 'react';
import type { User } from '@supabase/supabase-js';
import { supabase } from '../../api/supabaseClient';

export const AuthStatus = (): ReactElement => {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        supabase.auth.getUser().then(({ data }) => {
            setUser(data.user);
        });

        const { data: authListener } = supabase.auth.onAuthStateChange((_event, session) => {
            setUser(session?.user ?? null);
        });

        return () => {
            authListener.subscription.unsubscribe();
        };
    }, []);

    const handleLogin = async (): Promise<void> => {
        // For simplicity, we'll use OAuth or Magic Link.
        // Adjust this to your preferred auth method, e.g., GitHub or Google
        const email = prompt('Enter email for magic link login:', 'initiate@Synarche.com');
        if (!email) return;

        const { error } = await supabase.auth.signInWithOtp({
            email,
        });
        if (error) alert(error.message);
        else alert('Magic link sent! Check your email.');
    };

    const handleLogout = async (): Promise<void> => {
        await supabase.auth.signOut();
    };

    return (
        <div
            style={{ position: 'fixed', top: 10, right: 10, zIndex: 1000, fontFamily: 'monospace' }}
        >
            {user ? (
                <div style={{ background: '#111', padding: '5px 10px', border: '1px solid #333' }}>
                    <span style={{ color: '#4ade80', marginRight: 10 }}>● {user.email}</span>
                    <button
                        onClick={handleLogout}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: '#666',
                            cursor: 'pointer',
                        }}
                    >
                        LOGOUT
                    </button>
                </div>
            ) : (
                <button
                    onClick={handleLogin}
                    style={{
                        background: '#000',
                        color: '#fff',
                        border: '1px solid #fff',
                        padding: '5px 10px',
                        cursor: 'pointer',
                    }}
                >
                    INITIATE LOGIN
                </button>
            )}
        </div>
    );
};
