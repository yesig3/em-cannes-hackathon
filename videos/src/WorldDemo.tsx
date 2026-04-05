import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { c, slideUp, fade, TitleScene, WhatIsEM, TextSlide, LiveURLs, EndScene } from "./shared";

const FPS = 30;
const SEC = FPS;

// ============ SCENE: THE PROBLEM ============
const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 20);

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 900, textAlign: "center" }}>
        <h2 style={{ color: c.white, fontSize: 44, fontWeight: 800, margin: 0, opacity: s, transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)` }}>
          The Problem
        </h2>
        <p style={{ color: c.muted, fontSize: 28, lineHeight: 1.6, marginTop: 30, opacity: s2, transform: `translateY(${interpolate(s2, [0, 1], [30, 0])}px)` }}>
          AI agents pay humans for real-world tasks. But how do you know the worker is actually <span style={{ color: c.amber, fontWeight: 700 }}>a unique human</span> and not a bot farming bounties?
        </p>
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: WORLD ID FLOW ============
const WorldIdFlow: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const steps = [
    { icon: "1", text: "Worker clicks Apply on a task >= $5", color: c.white },
    { icon: "X", text: "Modal: Identity verification required", color: c.red },
    { icon: "W", text: "Worker verifies with World ID Orb", color: c.worldBlack },
    { icon: "V", text: "Backend verifies via Cloud API v4 + RP signing", color: c.cyan },
    { icon: "!", text: "Anti-sybil: 1 nullifier = 1 account", color: c.amber },
    { icon: "OK", text: "Worker can now apply — success shown in-modal", color: c.green },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 40, opacity: fade(frame, 0, 10) }}>
          World ID 4.0 — Enforcement Flow
        </h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {steps.map((step, i) => {
            const si = slideUp(frame, fps, 10 + i * 12);
            return (
              <div key={i} style={{
                display: "flex", alignItems: "center", gap: 20,
                backgroundColor: c.card, borderRadius: 14, padding: "18px 24px",
                border: `1px solid ${c.border}`,
                opacity: si, transform: `translateX(${interpolate(si, [0, 1], [60, 0])}px)`,
              }}>
                <div style={{
                  width: 44, height: 44, borderRadius: 10,
                  backgroundColor: `${step.color}20`, display: "flex",
                  alignItems: "center", justifyContent: "center",
                  color: step.color, fontSize: 18, fontWeight: 900,
                }}>{step.icon}</div>
                <span style={{ color: c.white, fontSize: 24 }}>{step.text}</span>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: ENFORCEMENT DIAGRAM ============
const EnforcementDiagram: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 15);
  const s3 = slideUp(frame, fps, 30);

  const paths = [
    { label: "Web Dashboard", icon: "UI" },
    { label: "REST API", icon: "API" },
    { label: "MCP Protocol", icon: "MCP" },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ textAlign: "center", maxWidth: 1000 }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, margin: "0 0 20px 0", opacity: s }}>
          Enforced at Every Entry Point
        </h2>
        <p style={{ color: c.muted, fontSize: 22, margin: "0 0 50px 0", opacity: s }}>
          One shared utility — all paths covered
        </p>

        <div style={{ display: "flex", justifyContent: "center", gap: 30, marginBottom: 30, opacity: s2, transform: `translateY(${interpolate(s2, [0, 1], [30, 0])}px)` }}>
          {paths.map((p) => (
            <div key={p.label} style={{
              backgroundColor: c.card, borderRadius: 14, padding: "20px 36px",
              border: `1px solid ${c.border}`, textAlign: "center",
            }}>
              <div style={{ color: c.violet, fontSize: 24, fontWeight: 900 }}>{p.icon}</div>
              <div style={{ color: c.white, fontSize: 18, marginTop: 8 }}>{p.label}</div>
            </div>
          ))}
        </div>

        <div style={{ color: c.muted, fontSize: 40, marginBottom: 20, opacity: s3 }}>v</div>

        <div style={{
          backgroundColor: `${c.worldBlack}`, borderRadius: 16,
          padding: "24px 48px", border: `2px solid ${c.white}40`,
          display: "inline-block", opacity: s3,
          transform: `translateY(${interpolate(s3, [0, 1], [20, 0])}px)`,
        }}>
          <span style={{ color: c.white, fontSize: 26, fontWeight: 700 }}>
            check_world_id_eligibility()
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============ SCENE: AGENTKIT ============
const AgentKitScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 15);

  return (
    <AbsoluteFill style={{ backgroundColor: c.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 60px" }}>
        <h2 style={{ color: c.white, fontSize: 40, fontWeight: 800, marginBottom: 40, opacity: s }}>
          AgentKit — Human vs Bot Gateway
        </h2>

        <div style={{ display: "flex", gap: 30, opacity: s2, transform: `translateY(${interpolate(s2, [0, 1], [40, 0])}px)` }}>
          <div style={{ flex: 1, backgroundColor: c.card, borderRadius: 16, padding: 36, border: `2px solid ${c.green}40` }}>
            <div style={{ color: c.green, fontSize: 28, fontWeight: 800, marginBottom: 16 }}>Human</div>
            <p style={{ color: c.white, fontSize: 22, margin: "0 0 12px 0" }}>AgentBook: humanId &gt; 0</p>
            <div style={{ backgroundColor: `${c.green}20`, borderRadius: 10, padding: "12px 20px", display: "inline-block" }}>
              <span style={{ color: c.green, fontSize: 22, fontWeight: 700 }}>FREE ACCESS</span>
            </div>
          </div>

          <div style={{ flex: 1, backgroundColor: c.card, borderRadius: 16, padding: 36, border: `2px solid ${c.red}40` }}>
            <div style={{ color: c.red, fontSize: 28, fontWeight: 800, marginBottom: 16 }}>Bot</div>
            <p style={{ color: c.white, fontSize: 22, margin: "0 0 12px 0" }}>AgentBook: humanId = 0</p>
            <div style={{ backgroundColor: `${c.red}20`, borderRadius: 10, padding: "12px 20px", display: "inline-block" }}>
              <span style={{ color: c.red, fontSize: 22, fontWeight: 700 }}>x402 PAYWALL $0.001</span>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============ MAIN COMPOSITION ============
export const WorldDemo: React.FC = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={5 * SEC}><TitleScene sponsor="World" sponsorColor={c.worldBlack} tracks={["World ID 4.0", "AgentKit"]} /></Sequence>
      <Sequence from={5 * SEC} durationInFrames={6 * SEC}><WhatIsEM /></Sequence>
      <Sequence from={11 * SEC} durationInFrames={6 * SEC}><ProblemScene /></Sequence>
      <Sequence from={17 * SEC} durationInFrames={12 * SEC}><WorldIdFlow /></Sequence>
      <Sequence from={29 * SEC} durationInFrames={8 * SEC}><EnforcementDiagram /></Sequence>
      <Sequence from={37 * SEC} durationInFrames={5 * SEC}>
        <TextSlide accent={c.cyan} title="Tech Stack" bullets={[
          "RP signing: secp256k1 + EIP-191 (from scratch)",
          "Cloud API v4: POST developer.world.org/api/v4/verify",
          "IDKit v4 with Orb preset (React)",
          "Anti-sybil: UNIQUE nullifier_hash in DB",
        ]} />
      </Sequence>
      <Sequence from={42 * SEC} durationInFrames={8 * SEC}><AgentKitScene /></Sequence>
      <Sequence from={50 * SEC} durationInFrames={7 * SEC}>
        <LiveURLs sponsorColor={c.worldBlack} urls={[
          { label: "Live Product", url: "execution.market" },
          { label: "Try Apply Flow", url: "execution.market (task >= $5)" },
          { label: "AgentBook", url: "basescan.org/address/0xE1D1D352..." },
          { label: "Hackathon Repo", url: "github.com/UltravioletaDAO/em-cannes-hackathon" },
        ]} />
      </Sequence>
      <Sequence from={57 * SEC} durationInFrames={5 * SEC}><EndScene sponsorColor={c.worldBlack} /></Sequence>
    </AbsoluteFill>
  );
};
