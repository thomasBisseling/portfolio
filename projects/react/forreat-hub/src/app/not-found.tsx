import { FaceFrownIcon } from "@heroicons/react/24/outline";

export default function NotFound() {
  return (
    <div className="not-found text-black flex flex-col items-center justify-center h-full relative">
      <h1 className="text-4xl absolute top-[15%] flex items-center gap-2 flex-col">
        <FaceFrownIcon className={"stroke-primary"} width={150} height={150} />
        404 - Pagina niet gevonden
      </h1>
    </div>
  );
}
