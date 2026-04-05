import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { c, slideUp, fade, TitleScene, WhatIsEM, TextSlide, LiveURLs, EndScene } from "./shared";

const FPS = 30;
const SEC = FPS;

// ============ SCENE: CROSS-CHAIN ARCHITECTURE ============
const CrossChainScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 20);
  const s3 = slideUp(frame, fps, 35);

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, textAlign: "center" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, margin: "0 0 50px 0", opacity: s }}>
          Cross-Chain Architecture
        </h2>

        <div style={{ display: "flex", justifyContent: "center", gap: 60, alignItems: "center" }}>
          <div style={{
            backgroundColor: c.card, borderRadius: 20, padding: "30px 40px",
            border: `2px solid ${c.cyan}40`, textAlign: "center",
            opacity: s2, transform: `translateX(${interpolate(s2, [0, 1], [-40, 0])}px)`,
          }}>
            <div style={{ color: c.cyan, fontSize: 28, fontWeight: 800 }}>Base</div>
            <div style={{ color: c.muted, fontSize: 18, marginTop: 8 }}>USDC Escrow</div>
            <div style={{ color: c.muted, fontSize: 18 }}>Payments</div>
          </div>

          <div style={{ color: c.muted, fontSize: 48, opacity: s3 }}>+</div>

          <div style={{
            backgroundColor: c.card, borderRadius: 20, padding: "30px 40px",
            border: `2px solid ${c.hederaPurple}40`, textAlign: "center",
            opacity: s2, transform: `translateX(${interpolate(s2, [0, 1], [40, 0])}px)`,
          }}>
            <div style={{ color: c.hederaPurple, fontSize: 28, fontWeight: 800 }}>Hedera</div>
            <div style={{ color: c.muted, fontSize: 18, marginTop: 8 }}>Identity + Reputation</div>
            <div style={{ color: c.muted, fontSize: 18 }}>HCS + Tips</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: 5 INTEGRATIONS ============
const FiveIntegrations: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const integrations = [
    { num: "1", name: "ERC-8004 Identity", detail: "Agent #99 on Hedera Testnet", color: c.hederaPurple },
    { num: "2", name: "Bidirectional Reputation", detail: "Agent rates worker, worker rates agent", color: c.green },
    { num: "3", name: "Merit Tips", detail: "0.01 HBAR to workers with rep > 80", color: c.amber },
    { num: "4", name: "HCS Event Logging", detail: "6 lifecycle events — Hedera-native, NOT EVM", color: c.cyan },
    { num: "5", name: "Facilitator Extension", detail: "Open-source Rust — Hedera support added", color: c.violet },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 36, opacity: fade(frame, 0, 10) }}>
          5 Hedera Integrations
        </h2>
        {integrations.map((item, i) => {
          const si = slideUp(frame, fps, 8 + i * 10);
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", gap: 20, marginBottom: 14,
              backgroundColor: c.card, borderRadius: 14, padding: "16px 24px",
              border: `1px solid ${c.border}`,
              opacity: si, transform: `translateX(${interpolate(si, [0, 1], [50, 0])}px)`,
            }}>
              <div style={{
                width: 40, height: 40, borderRadius: 10,
                backgroundColor: `${item.color}20`, display: "flex",
                alignItems: "center", justifyContent: "center",
                color: item.color, fontSize: 20, fontWeight: 900,
              }}>{item.num}</div>
              <div>
                <span style={{ color: c.white, fontSize: 22, fontWeight: 700 }}>{item.name}</span>
                <span style={{ color: c.muted, fontSize: 18, marginLeft: 16 }}>{item.detail}</span>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: HCS DETAIL ============
const HCSDetail: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);

  const events = [
    "task_created", "worker_applied", "task_assigned",
    "evidence_submitted", "task_completed", "payment_released",
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 12, opacity: s }}>
          HCS — Hedera Consensus Service
        </h2>
        <p style={{ color: c.cyan, fontSize: 22, marginBottom: 36, opacity: s }}>
          Hedera-native (NOT EVM) — immutable, consensus-timestamped
        </p>

        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, opacity: slideUp(frame, fps, 15) }}>
          {events.map((evt, i) => {
            const si = slideUp(frame, fps, 15 + i * 6);
            return (
              <div key={evt} style={{
                backgroundColor: c.card, borderRadius: 10, padding: "14px 22px",
                border: `1px solid ${c.hederaPurple}30`,
                opacity: si, transform: `translateY(${interpolate(si, [0, 1], [20, 0])}px)`,
              }}>
                <span style={{ color: c.hederaPurple, fontSize: 18, fontFamily: "monospace" }}>{evt}</span>
              </div>
            );
          })}
        </div>

        <div style={{ marginTop: 36, opacity: slideUp(frame, fps, 50) }}>
          <p style={{ color: c.muted, fontSize: 18, fontFamily: "monospace" }}>
            Topic: 0.0.8511429 — verifiable via Mirror Node REST API (no auth needed)
          </p>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: GOLDEN FLOW ============
const GoldenFlow: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const phases = [
    { phase: "1", label: "Escrow Lock", chain: "Base", status: "PASS" },
    { phase: "2", label: "Worker + Evidence", chain: "Base API", status: "PASS" },
    { phase: "3", label: "Payment Release", chain: "Base", status: "PASS" },
    { phase: "4", label: "Agent -> Worker Rep", chain: "Hedera", status: "PASS" },
    { phase: "5", label: "Worker -> Agent Rep", chain: "Hedera", status: "PASS" },
    { phase: "6", label: "Merit Tip (0.01 HBAR)", chain: "Hedera", status: "PASS" },
    { phase: "7", label: "HCS Event Log (6 msgs)", chain: "Hedera Native", status: "PASS" },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 36, opacity: fade(frame, 0, 10) }}>
          Golden Flow — 7/7 PASS
        </h2>
        {phases.map((p, i) => {
          const si = slideUp(frame, fps, 8 + i * 8);
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", gap: 16, marginBottom: 10,
              opacity: si, transform: `translateX(${interpolate(si, [0, 1], [40, 0])}px)`,
            }}>
              <div style={{
                width: 36, height: 36, borderRadius: 8,
                backgroundColor: `${c.green}20`, display: "flex",
                alignItems: "center", justifyContent: "center",
                color: c.green, fontSize: 16, fontWeight: 900,
              }}>{p.phase}</div>
              <span style={{ color: c.white, fontSize: 20, flex: 1 }}>{p.label}</span>
              <span style={{
                color: p.chain.includes("Hedera") ? c.hederaPurple : c.cyan,
                fontSize: 16, fontFamily: "monospace", minWidth: 140,
              }}>{p.chain}</span>
              <span style={{ color: c.green, fontSize: 18, fontWeight: 700 }}>{p.status}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============ MAIN COMPOSITION ============
export const HederaDemo: React.FC = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={5 * SEC}><TitleScene sponsor="Hedera" sponsorColor={c.hederaPurple} tracks={["AI & Agentic Payments"]} /></Sequence>
      <Sequence from={5 * SEC} durationInFrames={6 * SEC}><WhatIsEM /></Sequence>
      <Sequence from={11 * SEC} durationInFrames={7 * SEC}><CrossChainScene /></Sequence>
      <Sequence from={18 * SEC} durationInFrames={12 * SEC}><FiveIntegrations /></Sequence>
      <Sequence from={30 * SEC} durationInFrames={10 * SEC}><HCSDetail /></Sequence>
      <Sequence from={40 * SEC} durationInFrames={12 * SEC}><GoldenFlow /></Sequence>
      <Sequence from={52 * SEC} durationInFrames={7 * SEC}>
        <LiveURLs sponsorColor={c.hederaPurple} urls={[
          { label: "Live Product", url: "execution.market" },
          { label: "HCS Messages", url: "mirrornode.hedera.com/api/v1/topics/0.0.8511429" },
          { label: "Merit Tip TX", url: "hashscan.io/testnet/transaction/0x1c4ce9dc..." },
          { label: "Agent Identity", url: "facilitator.ultravioletadao.xyz/identity/hedera-testnet/99" },
          { label: "Facilitator Commit", url: "github.com/UltravioletaDAO/x402-rs/commit/66d34e6" },
        ]} />
      </Sequence>
      <Sequence from={59 * SEC} durationInFrames={5 * SEC}><EndScene sponsorColor={c.hederaPurple} /></Sequence>
    </AbsoluteFill>
  );
};
