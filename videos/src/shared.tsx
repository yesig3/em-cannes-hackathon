import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

// ============ PALETTE ============
export const c = {
  bg: "#09090B",
  card: "#18181B",
  violet: "#8B5CF6",
  cyan: "#06B6D4",
  green: "#10B981",
  red: "#EF4444",
  amber: "#F59E0B",
  white: "#FAFAFA",
  muted: "#71717A",
  border: "#27272A",
  worldBlack: "#191C20",
  hederaPurple: "#8259EF",
  ensBlue: "#5298FF",
};

// ============ HELPERS ============
export const fade = (frame: number, start: number, dur: number) =>
  interpolate(frame, [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const fadeOut = (frame: number, start: number, dur: number) =>
  interpolate(frame, [start, start + dur], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const slideUp = (frame: number, fps: number, delay = 0) =>
  spring({
    frame: Math.max(0, frame - delay),
    fps,
    config: { damping: 12, mass: 0.8 },
  });

// ============ SHARED SCENES ============

export const TitleScene: React.FC<{
  sponsor: string;
  sponsorColor: string;
  tracks: string[];
}> = ({ sponsor, sponsorColor, tracks }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 15);
  const s3 = slideUp(frame, fps, 30);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: c.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          textAlign: "center",
          transform: `translateY(${interpolate(s, [0, 1], [60, 0])}px)`,
          opacity: s,
        }}
      >
        <p
          style={{
            color: c.muted,
            fontSize: 24,
            letterSpacing: 6,
            textTransform: "uppercase",
            margin: 0,
          }}
        >
          ETHGlobal Cannes 2026
        </p>
      </div>

      <div
        style={{
          textAlign: "center",
          marginTop: 30,
          transform: `translateY(${interpolate(s2, [0, 1], [60, 0])}px)`,
          opacity: s2,
        }}
      >
        <h1
          style={{
            color: c.white,
            fontSize: 72,
            fontWeight: 900,
            margin: 0,
            lineHeight: 1.1,
          }}
        >
          Execution Market
        </h1>
        <h2
          style={{
            fontSize: 48,
            fontWeight: 700,
            margin: "10px 0 0 0",
            color: sponsorColor,
          }}
        >
          x {sponsor}
        </h2>
      </div>

      <div
        style={{
          marginTop: 40,
          display: "flex",
          gap: 16,
          transform: `translateY(${interpolate(s3, [0, 1], [40, 0])}px)`,
          opacity: s3,
        }}
      >
        {tracks.map((track) => (
          <div
            key={track}
            style={{
              padding: "10px 24px",
              borderRadius: 100,
              border: `1px solid ${sponsorColor}60`,
              backgroundColor: `${sponsorColor}15`,
              color: sponsorColor,
              fontSize: 20,
              fontWeight: 600,
            }}
          >
            {track}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const WhatIsEM: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 20);

  const features = [
    { icon: "AI", label: "AI agents publish bounties", color: c.violet },
    { icon: ">>", label: "Human workers execute", color: c.green },
    { icon: "$", label: "Instant gasless payment (x402)", color: c.cyan },
    { icon: "#", label: "On-chain reputation", color: c.amber },
  ];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: c.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ maxWidth: 1100, width: "100%", padding: "0 60px" }}>
        <div
          style={{
            transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
            opacity: s,
          }}
        >
          <p
            style={{
              color: c.muted,
              fontSize: 20,
              textTransform: "uppercase",
              letterSpacing: 4,
              margin: "0 0 12px 0",
            }}
          >
            What is Execution Market?
          </p>
          <h2
            style={{
              color: c.white,
              fontSize: 44,
              fontWeight: 800,
              margin: "0 0 50px 0",
            }}
          >
            The Universal Execution Layer
          </h2>
        </div>

        <div style={{ display: "flex", gap: 20 }}>
          {features.map((f, i) => {
            const si = slideUp(frame, fps, 20 + i * 10);
            return (
              <div
                key={f.label}
                style={{
                  flex: 1,
                  backgroundColor: c.card,
                  borderRadius: 16,
                  padding: "30px 24px",
                  border: `1px solid ${c.border}`,
                  transform: `translateY(${interpolate(si, [0, 1], [40, 0])}px)`,
                  opacity: si,
                }}
              >
                <div
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: 12,
                    backgroundColor: `${f.color}20`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: f.color,
                    fontSize: 20,
                    fontWeight: 900,
                    marginBottom: 16,
                  }}
                >
                  {f.icon}
                </div>
                <p
                  style={{
                    color: c.white,
                    fontSize: 20,
                    margin: 0,
                    lineHeight: 1.4,
                  }}
                >
                  {f.label}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const LiveURLs: React.FC<{
  urls: { label: string; url: string }[];
  sponsorColor: string;
}> = ({ urls, sponsorColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: c.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ maxWidth: 900, width: "100%", padding: "0 60px" }}>
        <h2
          style={{
            color: c.white,
            fontSize: 40,
            fontWeight: 800,
            marginBottom: 40,
            opacity: s,
          }}
        >
          Verify It Live
        </h2>
        {urls.map((u, i) => {
          const si = slideUp(frame, fps, 10 + i * 8);
          return (
            <div
              key={u.label}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 20,
                padding: "18px 0",
                borderBottom: `1px solid ${c.border}`,
                transform: `translateY(${interpolate(si, [0, 1], [30, 0])}px)`,
                opacity: si,
              }}
            >
              <span
                style={{
                  color: sponsorColor,
                  fontSize: 22,
                  fontWeight: 700,
                  minWidth: 240,
                }}
              >
                {u.label}
              </span>
              <span style={{ color: c.muted, fontSize: 18, fontFamily: "monospace" }}>
                {u.url}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const EndScene: React.FC<{ sponsorColor: string }> = ({
  sponsorColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);
  const s2 = slideUp(frame, fps, 15);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: c.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          textAlign: "center",
          transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
          opacity: s,
        }}
      >
        <h1
          style={{ color: c.white, fontSize: 64, fontWeight: 900, margin: 0 }}
        >
          execution.market
        </h1>
        <p
          style={{
            color: sponsorColor,
            fontSize: 28,
            marginTop: 16,
            opacity: s2,
          }}
        >
          Universal Execution Layer — from LATAM to the world
        </p>
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 60,
          display: "flex",
          gap: 40,
          opacity: s2,
        }}
      >
        <span style={{ color: c.muted, fontSize: 18 }}>
          github.com/UltravioletaDAO
        </span>
        <span style={{ color: c.muted, fontSize: 18 }}>@ExecutionMarket</span>
        <span style={{ color: c.muted, fontSize: 18 }}>Agent #2106</span>
      </div>
    </AbsoluteFill>
  );
};

export const TextSlide: React.FC<{
  title: string;
  bullets: string[];
  accent: string;
}> = ({ title, bullets, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = slideUp(frame, fps);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: c.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ maxWidth: 1000, width: "100%", padding: "0 80px" }}>
        <h2
          style={{
            color: c.white,
            fontSize: 44,
            fontWeight: 800,
            marginBottom: 40,
            opacity: s,
            transform: `translateY(${interpolate(s, [0, 1], [30, 0])}px)`,
          }}
        >
          {title}
        </h2>
        {bullets.map((b, i) => {
          const si = slideUp(frame, fps, 10 + i * 8);
          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "flex-start",
                gap: 16,
                marginBottom: 24,
                opacity: si,
                transform: `translateY(${interpolate(si, [0, 1], [20, 0])}px)`,
              }}
            >
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: accent,
                  marginTop: 12,
                  flexShrink: 0,
                }}
              />
              <p
                style={{
                  color: c.white,
                  fontSize: 28,
                  margin: 0,
                  lineHeight: 1.5,
                }}
              >
                {b}
              </p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
