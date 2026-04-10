import { trustItems } from '../data/products';

export function TrustMarquee() {
  // Duplicate list for seamless loop
  const items = [...trustItems, ...trustItems];

  return (
    <section className="relative border-y border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] py-6">
      <div className="pointer-events-none absolute inset-y-0 left-0 z-10 w-24 bg-gradient-to-r from-[color:var(--color-ink-800)] to-transparent" />
      <div className="pointer-events-none absolute inset-y-0 right-0 z-10 w-24 bg-gradient-to-l from-[color:var(--color-ink-800)] to-transparent" />
      <div className="flex overflow-hidden">
        <div className="marquee-track flex shrink-0 items-center gap-12 pr-12">
          {items.map((item, i) => (
            <div key={`${item}-${i}`} className="flex shrink-0 items-center gap-12">
              <div className="flex items-center gap-3">
                <span className="h-1.5 w-1.5 rotate-45 bg-[color:var(--color-amber-base)]" />
                <span className="text-sm font-black uppercase tracking-[0.18em] text-[color:var(--color-ink-100)] md:text-base">
                  {item}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
