import { Composition } from "remotion";
import { WorldDemo } from "./WorldDemo";
import { HederaDemo } from "./HederaDemo";
import { ENSDemo } from "./ENSDemo";

const FPS = 30;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="WorldDemo"
      component={WorldDemo}
      durationInFrames={62 * FPS}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="HederaDemo"
      component={HederaDemo}
      durationInFrames={64 * FPS}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="ENSDemo"
      component={ENSDemo}
      durationInFrames={67 * FPS}
      fps={FPS}
      width={1920}
      height={1080}
    />
  </>
);
