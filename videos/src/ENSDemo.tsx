import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { c, slideUp, fade, TitleScene, WhatIsEM, TextSlide, LiveURLs, EndScene } from "./shared";

const FPS = 30;
const SEC = FPS;

// ============ SCENE: ENS DOMAIN ============
const ENSDomainScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 20);

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ textAlign: "center", maxWidth: 900 }}>
        <p style={{ color: c.muted, fontSize: 20, textTransform: "uppercase", letterSpacing: 4, margin: "0 0 20px 0", opacity: s }}>
          Registered on Ethereum Mainnet
        </p>
        <h1 style={{
          color: c.white, fontSize: 72, fontWeight: 900, margin: 0,
          opacity: s, transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
        }}>
          <span style={{ color: c.ensBlue }}>execution-market</span>.eth
        </h1>
        <p style={{ color: c.muted, fontSize: 24, marginTop: 20, opacity: s2 }}>
          Agent #2106 — discoverable by humans and machines
        </p>
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: TEXT RECORDS ============
const TextRecordsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const records = [
    { key: "url", value: "https://execution.market" },
    { key: "description", value: "Universal Execution Layer" },
    { key: "avatar", value: "https://execution.market/logo.png" },
    { key: "com.twitter", value: "@ExecutionMarket" },
    { key: "com.execution.market.agentId", value: "2106" },
    { key: "com.execution.market.role", value: "platform" },
    { key: "com.execution.market.chains", value: "base,ethereum,polygon,..." },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 36, opacity: fade(frame, 0, 10) }}>
          7 On-Chain Text Records (ENSIP-5)
        </h2>
        {records.map((r, i) => {
          const si = slideUp(frame, fps, 8 + i * 7);
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", gap: 16, marginBottom: 10,
              padding: "12px 0", borderBottom: `1px solid ${c.border}`,
              opacity: si, transform: `translateX(${interpolate(si, [0, 1], [40, 0])}px)`,
            }}>
              <span style={{ color: c.ensBlue, fontSize: 18, fontFamily: "monospace", minWidth: 340, fontWeight: 600 }}>{r.key}</span>
              <span style={{ color: c.muted, fontSize: 18, fontFamily: "monospace" }}>{r.value}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: WORKER SUBNAMES ============
const SubnamesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);

  const workers = [
    { name: "alice.execution-market.eth", wallet: "0x1a2b...3c4d", rep: 92 },
    { name: "bob.execution-market.eth", wallet: "0x5e6f...7g8h", rep: 87 },
    { name: "carlos.execution-market.eth", wallet: "0x9i0j...1k2l", rep: 95 },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 12, opacity: s }}>
          Worker Subnames
        </h2>
        <p style={{ color: c.muted, fontSize: 22, marginBottom: 40, opacity: s }}>
          Human-readable identity via NameWrapper
        </p>

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {workers.map((w, i) => {
            const si = slideUp(frame, fps, 15 + i * 10);
            return (
              <div key={i} style={{
                backgroundColor: c.card, borderRadius: 16, padding: "24px 30px",
                border: `1px solid ${c.border}`, display: "flex", alignItems: "center", gap: 20,
                opacity: si, transform: `translateY(${interpolate(si, [0, 1], [30, 0])}px)`,
              }}>
                <div style={{
                  width: 48, height: 48, borderRadius: "50%",
                  background: `linear-gradient(135deg, ${c.ensBlue}, ${c.violet})`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  color: c.white, fontSize: 20, fontWeight: 900,
                }}>{w.name[0].toUpperCase()}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ color: c.ensBlue, fontSize: 22, fontWeight: 700 }}>{w.name}</div>
                  <div style={{ color: c.muted, fontSize: 16, fontFamily: "monospace" }}>{w.wallet}</div>
                </div>
                <div style={{ color: c.amber, fontSize: 20, fontWeight: 700 }}>Rep: {w.rep}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: AUTO-DETECTION FLOW ============
const AutoDetectFlow: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const steps = [
    { num: "1", text: "Worker connects wallet", color: c.white },
    { num: "2", text: "Backend: reverse ENS lookup (address -> name)", color: c.ensBlue },
    { num: "3", text: "ENS badge appears on profile automatically", color: c.green },
    { num: "4", text: "Badge shown on task applications", color: c.cyan },
    { num: "5", text: "Other agents query text records programmatically", color: c.violet },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 36, opacity: fade(frame, 0, 10) }}>
          Auto-Detection Flow
        </h2>
        {steps.map((step, i) => {
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
                backgroundColor: `${step.color}20`, display: "flex",
                alignItems: "center", justifyContent: "center",
                color: step.color, fontSize: 18, fontWeight: 900,
              }}>{step.num}</div>
              <span style={{ color: c.white, fontSize: 22 }}>{step.text}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: CREATIVE ANGLE ============
const CreativeAngle: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 20);

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 900, textAlign: "center" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, margin: "0 0 30px 0", opacity: s }}>
          ENS as AI Agent Identity
        </h2>
        <p style={{ color: c.muted, fontSize: 26, lineHeight: 1.6, opacity: s2, transform: `translateY(${interpolate(s2, [0, 1], [30, 0])}px)` }}>
          Other agents can query <span style={{ color: c.ensBlue, fontWeight: 700 }}>execution-market.eth</span> text records to discover our <span style={{ color: c.amber }}>agent ID</span>, <span style={{ color: c.green }}>supported chains</span>, and <span style={{ color: c.violet }}>capabilities</span> — making ENS a <span style={{ color: c.white, fontWeight: 700 }}>machine-readable directory</span> for the agentic web.
        </p>
      </div>
    </AbsoluteFill>
  );
};

// ============ MAIN COMPOSITION ============
export const ENSDemo: React.FC = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={5 * SEC}><TitleScene sponsor="ENS" sponsorColor={c.ensBlue} tracks={["Best Integration for AI Agents", "Most Creative Use"]} /></Sequence>
      <Sequence from={5 * SEC} durationInFrames={6 * SEC}><WhatIsEM /></Sequence>
      <Sequence from={11 * SEC} durationInFrames={7 * SEC}><ENSDomainScene /></Sequence>
      <Sequence from={18 * SEC} durationInFrames={10 * SEC}><TextRecordsScene /></Sequence>
      <Sequence from={28 * SEC} durationInFrames={10 * SEC}><SubnamesScene /></Sequence>
      <Sequence from={38 * SEC} durationInFrames={10 * SEC}><AutoDetectFlow /></Sequence>
      <Sequence from={48 * SEC} durationInFrames={7 * SEC}><CreativeAngle /></Sequence>
      <Sequence from={55 * SEC} durationInFrames={7 * SEC}>
        <LiveURLs sponsorColor={c.ensBlue} urls={[
          { label: "Live Product", url: "execution.market" },
          { label: "ENS Domain", url: "app.ens.domains/execution-market.eth" },
          { label: "API Resolve", url: "api.execution.market/api/v1/ens/resolve" },
          { label: "Hackathon Repo", url: "github.com/UltravioletaDAO/em-cannes-hackathon" },
        ]} />
      </Sequence>
      <Sequence from={62 * SEC} durationInFrames={5 * SEC}><EndScene sponsorColor={c.ensBlue} /></Sequence>
    </AbsoluteFill>
  );
};
