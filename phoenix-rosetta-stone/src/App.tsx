import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { DashboardView } from "@/components/views/Dashboard";
import { MemoryPalaceView } from "@/components/views/MemoryPalace";
import { RPGCommandView } from "@/components/views/RPGCommand";
import { KnowledgeForgeView } from "@/components/views/KnowledgeForge";
import { ChronicleView } from "@/components/views/Chronicle";
import { NotificationsView } from "@/components/views/Notifications";
import { TarotForgeView } from "@/components/views/TarotForge";
import { NeoGenesisView } from "@/components/views/NeoGenesis";
import { ToastContainer } from "@/components/ui/Toast";

export default function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<DashboardView />} />
          <Route path="/memory" element={<MemoryPalaceView />} />
          <Route path="/rpg" element={<RPGCommandView />} />
          <Route path="/knowledge" element={<KnowledgeForgeView />} />
          <Route path="/chronicle" element={<ChronicleView />} />
          <Route path="/notifications" element={<NotificationsView />} />
          <Route path="/tarot" element={<TarotForgeView />} />
          <Route path="/evolution" element={<NeoGenesisView />} />
        </Routes>
      </AppShell>
      <ToastContainer />
    </BrowserRouter>
  );
}
