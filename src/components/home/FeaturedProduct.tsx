import { motion } from 'framer-motion';
import { ArrowRight, ShieldCheck, Plus } from 'lucide-react';
import { featuredProduct } from './homeData';

export function FeaturedProduct() {
  const addToBasket = () => {
    window.roamCart?.add(featuredProduct.cart);
  };

  return (
    <section id="frames" className="relative overflow-hidden bg-[color:var(--color-ink-900)] py-24 md:py-32">
      <div className="absolute inset-0 bg-grid bg-grid-fade opacity-30" />
      <div className="relative mx-auto max-w-7xl px-4 md:px-8">
        <div className="grid grid-cols-1 items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="relative"
          >
            <div className="relative aspect-[4/5] w-full overflow-hidden rounded-2xl border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)]">
              <img
                src={featuredProduct.image}
                alt={featuredProduct.name}
                className="h-full w-full object-cover"
                loading="lazy"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[color:var(--color-ink-900)]/60 via-transparent to-[color:var(--color-ink-900)]/30" />
              <div className="absolute left-4 top-4 flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-white drop-shadow">
                <span className="h-px w-6 bg-[color:var(--color-amber-base)]" />
                <span>Fig. 01</span>
              </div>
              <div className="absolute bottom-4 right-4 flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-white drop-shadow">
                <span>ECE 14.09</span>
                <span className="h-px w-6 bg-[color:var(--color-amber-base)]" />
              </div>
              <div className="absolute left-0 top-0 h-6 w-6 border-l-2 border-t-2 border-[color:var(--color-amber-base)]" />
              <div className="absolute right-0 top-0 h-6 w-6 border-r-2 border-t-2 border-[color:var(--color-amber-base)]" />
              <div className="absolute bottom-0 left-0 h-6 w-6 border-b-2 border-l-2 border-[color:var(--color-amber-base)]" />
              <div className="absolute bottom-0 right-0 h-6 w-6 border-b-2 border-r-2 border-[color:var(--color-amber-base)]" />
            </div>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="absolute -right-4 -top-4 rounded-lg border border-[color:var(--color-amber-base)] bg-[color:var(--color-ink-900)] px-5 py-4 shadow-[0_0_40px_rgba(232,126,4,0.35)] md:-right-8 md:-top-8"
            >
              <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-[color:var(--color-amber-base)]">From</div>
              <div className="font-black text-2xl text-white md:text-3xl">£{featuredProduct.price.toLocaleString()}</div>
              <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-ink-300)]">+ VAT</div>
            </motion.div>
          </motion.div>

          <div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 rounded-md border border-[color:var(--color-amber-base)] bg-[color:var(--color-amber-base)]/10 px-3 py-1.5"
            >
              <ShieldCheck className="h-4 w-4 text-[color:var(--color-amber-base)]" strokeWidth={2.5} />
              <span className="text-xs font-black uppercase tracking-[0.2em] text-[color:var(--color-amber-base)]">M1 Certified</span>
            </motion.div>

            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1, duration: 0.6 }}
              className="mt-6 font-black uppercase leading-[0.95] tracking-tightest text-white text-4xl md:text-5xl lg:text-6xl"
            >
              The only <span className="text-[color:var(--color-amber-base)]">M1 certified</span> U-shape seating system available
            </motion.h2>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="mt-6 max-w-lg text-[color:var(--color-ink-300)]"
            >
              {featuredProduct.description}
            </motion.p>

            <div className="mt-10 grid grid-cols-2 gap-3">
              {featuredProduct.specs.map((spec, i) => (
                <motion.div
                  key={spec.label}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: '-50px' }}
                  transition={{ delay: 0.3 + i * 0.1, duration: 0.5 }}
                  className="group relative overflow-hidden rounded-lg border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] p-5 transition-colors hover:border-[color:var(--color-amber-base)]"
                >
                  <div className="absolute left-0 top-0 h-full w-1 bg-[color:var(--color-amber-base)] opacity-0 transition-opacity group-hover:opacity-100" />
                  <div className="text-[10px] font-bold uppercase tracking-[0.18em] text-[color:var(--color-ink-300)]">{spec.label}</div>
                  <div className="mt-1 font-black text-2xl text-white">{spec.value}</div>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.8, duration: 0.5 }}
              className="mt-10 flex flex-wrap gap-3"
            >
              <a
                href={featuredProduct.href}
                className="group inline-flex items-center gap-3 rounded-md border border-[color:var(--color-ink-500)] bg-[color:var(--color-ink-800)] px-8 py-4 text-sm font-black uppercase tracking-wider text-white transition-all hover:border-[color:var(--color-amber-base)] hover:bg-[color:var(--color-ink-700)]"
              >
                View Full Details
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" strokeWidth={3} />
              </a>
              <button
                type="button"
                onClick={addToBasket}
                className="group inline-flex items-center gap-3 rounded-md bg-[color:var(--color-amber-base)] px-8 py-4 text-sm font-black uppercase tracking-wider text-black transition-all hover:bg-[color:var(--color-amber-bright)]"
              >
                Add to Basket
                <Plus className="h-4 w-4 transition-transform group-hover:rotate-90" strokeWidth={3} />
              </button>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
}
