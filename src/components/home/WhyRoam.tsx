import { motion } from 'framer-motion';
import { ShieldCheck, Cog, MapPin, Users } from 'lucide-react';

const features = [
  { Icon: ShieldCheck, title: 'M1 Certified Safety', body: 'ECE 14.09 certified seating with integrated 3-point seatbelts and ISOFIX points. The only M1 certified U-shape system in the UK.', meta: 'ECE 14.09' },
  { Icon: Cog, title: 'Precision Engineered', body: 'Laser-cut frames. CNC-machined joinery. Powder-coated finishes. Built to tolerances the caravan industry has never seen.', meta: '±0.2mm tolerance' },
  { Icon: MapPin, title: 'Designed & Made in the UK', body: 'Manufactured by Romark Engineering Ltd in Essex. Protected by EU Registered Community Design RCD 015033319.', meta: 'RCD 015033319' },
  { Icon: Users, title: 'Nationwide Support', body: 'A network of 17 approved installers from Essex to Scotland. Fit it yourself, or let a pro handle it.', meta: '17 Installers' },
];

export function WhyRoam() {
  return (
    <section id="why" className="relative bg-[color:var(--color-ink-800)] py-24 md:py-32">
      <div className="mx-auto max-w-7xl px-4 md:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 max-w-3xl"
        >
          <div className="flex items-center gap-3">
            <span className="h-px w-10 bg-[color:var(--color-amber-base)]" />
            <span className="text-xs font-black uppercase tracking-[0.2em] text-[color:var(--color-amber-base)]">Why ROAM</span>
          </div>
          <h2 className="mt-4 font-black uppercase leading-[0.9] tracking-tightest text-white text-4xl md:text-6xl">
            No compromise.<br />
            <span className="text-[color:var(--color-ink-400)]">Just engineering.</span>
          </h2>
        </motion.div>

        <div className="grid gap-4 md:grid-cols-2">
          {features.map((f, i) => {
            const Icon = f.Icon;
            return (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ delay: i * 0.12, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                className="group relative overflow-hidden rounded-xl border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-900)] p-8 transition-colors hover:border-[color:var(--color-amber-base)]"
              >
                <div className="absolute left-0 top-0 h-4 w-4 border-l-2 border-t-2 border-[color:var(--color-amber-base)] opacity-0 transition-opacity group-hover:opacity-100" />
                <div className="absolute right-0 top-0 h-4 w-4 border-r-2 border-t-2 border-[color:var(--color-amber-base)] opacity-0 transition-opacity group-hover:opacity-100" />
                <div className="absolute bottom-0 left-0 h-4 w-4 border-b-2 border-l-2 border-[color:var(--color-amber-base)] opacity-0 transition-opacity group-hover:opacity-100" />
                <div className="absolute bottom-0 right-0 h-4 w-4 border-b-2 border-r-2 border-[color:var(--color-amber-base)] opacity-0 transition-opacity group-hover:opacity-100" />

                <div className="flex items-start gap-6">
                  <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-lg border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)]">
                    <Icon className="h-6 w-6 text-[color:var(--color-amber-base)]" strokeWidth={2} />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between gap-4">
                      <h3 className="font-black uppercase tracking-tight text-white text-xl">{f.title}</h3>
                      <span className="shrink-0 rounded-sm border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-[color:var(--color-ink-300)]">
                        {f.meta}
                      </span>
                    </div>
                    <p className="mt-3 text-sm leading-relaxed text-[color:var(--color-ink-300)]">{f.body}</p>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
