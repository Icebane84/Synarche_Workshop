/**
 * @artifact src/core/hooks/useNotifications.ts
 * @relations
 * REF: useActionLog.ts
 * REF: useMemoryFeed.ts
 * Notifications feed with unread count and live INSERT subscription.
 */

import { useState, useCallback, useEffect } from "react";
import { supabase } from "@/core/supabase";
import { useRealtime } from "./useRealtime";
import type { Notification } from "@/core/supabase";

interface UseNotificationsResult {
  notifications: Notification[];
  unreadCount: number;
  isLoading: boolean;
  markRead: (id: string) => Promise<void>;
  markAllRead: () => Promise<void>;
}

export function useNotifications(): UseNotificationsResult {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetch = useCallback(async () => {
    const { data } = await supabase
      .from("notifications")
      .select("*")
      .order("created_at", { ascending: false })
      .limit(50);
    setNotifications(data ?? []);
    setIsLoading(false);
  }, []);

  useEffect(() => { fetch(); }, [fetch]);

  // New notifications stream in live
  useRealtime("notifications", "INSERT", (payload) => {
    const n = payload.new as Notification;
    setNotifications((prev) => [n, ...prev]);
  });

  const markRead = async (id: string) => {
    await supabase.from("notifications").update({ read: true }).eq("id", id);
    setNotifications((prev) => prev.map((n) => n.id === id ? { ...n, read: true } : n));
  };

  const markAllRead = async () => {
    await supabase.from("notifications").update({ read: true }).eq("read", false);
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  return {
    notifications,
    unreadCount: notifications.filter((n) => !n.read).length,
    isLoading,
    markRead,
    markAllRead,
  };
}
