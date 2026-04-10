import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import { products } from '../data/products';

export function ProductGrid() {
  return (
    <section id="products" className="relative bg-[color:var(--color-ink-800)] py-24 md:py-32">
      <div className="mx-auto max-w-7xl px-4 md:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-14 flex flex-col items-start justify-between gap-4 md:mb-20 md:flex-row md:items-end"
        >
          <div>
            <div className="flex items-center gap-3">
              <span className="h-px w-10 bg-[color:var(--color-amber-base)]" />
              <span className="text-xs font-black uppercase tracking-[0.2em] text-[color:var(--color-amber-base)]">
                The Range
              </span>
            </div>
            <h2 className="mt-3 font-black uppercase leading-[0.9] tracking-tightest text-white text-4xl md:text-6xl">
              Built to last.<br />
              <span className="text-[color:var(--color-ink-400)]">Priced to own.</span>
            </h2>
          </div>
          <p className="max-w-xs text-sm text-[color:var(--color-ink-300)]">
            Every item laser-cut and CNC-machined in Essex. No filler, no fluff — engineering only.
          </p>
        </motion.div>

        {/* Grid */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {products.map((product, i) => (
            <motion.article
              key={product.id}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{
                delay: (i % 3) * 0.08 + Math.floor(i / 3) * 0.15,
                duration: 0.6,
                ease: [0.22, 1, 0.36, 1],
              }}
              className="group relative flex flex-col overflow-hidden rounded-xl border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-900)] transition-all duration-300 hover:border-[color:var(--color-amber-base)]"
            >
              {/* Product image */}
              <div className="relative aspect-[4/3] w-full overflow-hidden bg-[color:var(--color-ink-800)]">
                <img
                  src={product.image}
                  alt={product.name}
                  className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                  loading="lazy"
                />
                {/* Subtle dark overlay so corner labels stay legible on any shot */}
                <div className="absolute inset-0 bg-gradient-to-b from-[color:var(--color-ink-900)]/60 via-transparent to-[color:var(--color-ink-900)]/30" />
                {/* Index marker */}
                <div className="absolute left-4 top-4 flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-white drop-shadow">
                  <span className="h-px w-4 bg-[color:var(--color-amber-base)]" />
                  <span>{String(i + 1).padStart(2, '0')} / {String(products.length).padStart(2, '0')}</span>
                </div>
                {/* Category pill */}
                <div className="absolute right-4 top-4 rounded-sm border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-900)]/80 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-[color:var(--color-ink-200)] backdrop-blur">
                  {product.category}
                </div>
                {/* Hover accent bar */}
                <div className="absolute bottom-0 left-0 h-1 w-0 bg-[color:var(--color-amber-base)] transition-all duration-500 group-hover:w-full" />
              </div>

              {/* Body */}
              <div className="flex flex-1 flex-col p-6">
                <h3 className="font-black uppercase leading-tight tracking-tight text-white text-lg">
                  {product.name}
                </h3>
                <p className="mt-2 flex-1 text-sm text-[color:var(--color-ink-300)]">
                  {product.blurb}
                </p>
                <div className="mt-5 flex items-end justify-between">
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-widest text-[color:var(--color-ink-400)]">
                      From
                    </div>
                    <div className="font-black text-2xl text-white">
                      £{product.price.toLocaleString()}
                      <span className="ml-1 text-xs font-normal text-[color:var(--color-ink-400)]">+ VAT</span>
                    </div>
                  </div>
                </div>
                <button
                  type="button"
                  className="group/btn mt-5 inline-flex items-center justify-between gap-2 rounded-md bg-[color:var(--color-amber-base)] px-5 py-3 text-xs font-black uppercase tracking-wider text-black transition-all hover:bg-[color:var(--color-amber-bright)]"
                >
                  Add to Basket
                  <Plus className="h-4 w-4 transition-transform group-hover/btn:rotate-90" strokeWidth={3} />
                </button>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
