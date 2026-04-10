import { motion } from 'framer-motion';
import { ArrowRight, Play } from 'lucide-react';
import { vehicles, heroImage } from '../data/products';

const wordVariants = {
  hidden: { y: '110%', opacity: 0 },
  show: (i: number) => ({
    y: 0,
    opacity: 1,
    transition: {
      delay: 0.15 + i * 0.12,
      duration: 0.7,
      ease: [0.22, 1, 0.36, 1],
    },
  }),
};

export function Hero() {
  return (
    <section id="top" className="relative flex min-h-screen items-center overflow-hidden pt-28 md:pt-32">
      {/* Dark industrial background layers */}
      <div className="absolute inset-0 bg-[color:var(--color-ink-900)]">
        {/* Real product hero image — right side */}
        <div className="absolute right-0 top-0 hidden h-full w-[60%] lg:block">
          <img
            src={heroImage}
            alt="M1 Certified U-Shape Seating Frame"
            className="h-full w-full object-cover object-center"
            loading="eager"
          />
        </div>
        {/* Mobile / tablet: full-bleed background image */}
        <img
          src={heroImage}
          alt=""
          aria-hidden
          className="absolute inset-0 h-full w-full object-cover object-center opacity-30 lg:hidden"
          loading="eager"
        />
        {/* Grid overlay */}
        <div className="absolute inset-0 bg-grid bg-grid-fade opacity-60 mix-blend-overlay" />
        {/* Amber glow accent */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-[80vh] w-[80vh] max-w-none rounded-full bg-gradient-to-br from-[color:var(--color-amber-base)]/15 via-transparent to-transparent blur-3xl" />
        </div>
        {/* Left-to-right dark gradient so the headline always reads */}
        <div className="absolute inset-0 bg-gradient-to-r from-[color:var(--color-ink-900)] via-[color:var(--color-ink-900)]/90 to-[color:var(--color-ink-900)]/20" />
        <div className="absolute inset-0 bg-gradient-to-t from-[color:var(--color-ink-900)] via-transparent to-[color:var(--color-ink-900)]/50" />
        {/* Bottom fade into next section */}
        <div className="absolute inset-x-0 bottom-0 h-48 bg-gradient-to-t from-[color:var(--color-ink-900)] to-transparent" />
      </div>

      <div className="relative mx-auto w-full max-w-7xl px-4 md:px-8">
        {/* Eyebrow */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.6 }}
          className="mb-6 inline-flex items-center gap-3 rounded-full border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)]/60 px-4 py-1.5 backdrop-blur"
        >
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[color:var(--color-amber-base)] opacity-60" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-[color:var(--color-amber-base)]" />
          </span>
          <span className="text-xs font-bold uppercase tracking-[0.2em] text-[color:var(--color-ink-200)]">
            Precision Engineered · Essex, UK
          </span>
        </motion.div>

        {/* Headline — staggered word reveal */}
        <h1 className="font-bold uppercase leading-[0.95] tracking-tight text-white">
          <span className="block overflow-hidden">
            <motion.span
              custom={0}
              initial="hidden"
              animate="show"
              variants={wordVariants}
              className="block text-[clamp(2.25rem,6.5vw,5rem)]"
            >
              Your Van.
            </motion.span>
          </span>
          <span className="block overflow-hidden">
            <motion.span
              custom={1}
              initial="hidden"
              animate="show"
              variants={wordVariants}
              className="block text-[clamp(2.25rem,6.5vw,5rem)] text-[color:var(--color-amber-base)]"
            >
              Your Way.
            </motion.span>
          </span>
        </h1>

        {/* Subheading */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.6 }}
          className="mt-8 max-w-xl text-base text-[color:var(--color-ink-200)] md:text-lg"
        >
          The UK's only <span className="font-semibold text-white">M1 certified U-shape seating system</span>. Precision-engineered in Essex.
        </motion.p>

        {/* Vehicle selector pills */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.85, duration: 0.6 }}
          className="mt-8 flex flex-wrap gap-2"
        >
          {vehicles.map((v, i) => (
            <motion.button
              key={v}
              type="button"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.9 + i * 0.05, duration: 0.3 }}
              whileHover={{ y: -2 }}
              className="rounded-md border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)]/70 px-3.5 py-2 text-xs font-bold uppercase tracking-wider text-[color:var(--color-ink-200)] backdrop-blur transition-colors hover:border-[color:var(--color-amber-base)] hover:text-white"
            >
              {v}
            </motion.button>
          ))}
        </motion.div>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.05, duration: 0.6 }}
          className="mt-10 flex flex-wrap gap-4"
        >
          <a
            href="#products"
            className="group inline-flex items-center gap-3 rounded-md bg-[color:var(--color-amber-base)] px-8 py-4 text-sm font-black uppercase tracking-wider text-black transition-all hover:bg-[color:var(--color-amber-bright)] hover:shadow-[0_0_40px_var(--color-amber-glow)]"
          >
            Shop Now
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" strokeWidth={3} />
          </a>
          <a
            href="#gallery"
            className="group inline-flex items-center gap-3 rounded-md border border-[color:var(--color-ink-500)] bg-[color:var(--color-ink-800)]/60 px-8 py-4 text-sm font-black uppercase tracking-wider text-white backdrop-blur transition-all hover:border-[color:var(--color-amber-base)] hover:text-[color:var(--color-amber-base)]"
          >
            <Play className="h-4 w-4" strokeWidth={2.5} />
            View Gallery
          </a>
        </motion.div>

        {/* Bottom meta strip */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.3, duration: 0.8 }}
          className="mt-16 flex flex-wrap items-center gap-x-8 gap-y-3 text-xs uppercase tracking-[0.18em] text-[color:var(--color-ink-300)] md:mt-24"
        >
          <div className="flex items-center gap-2">
            <span className="h-px w-8 bg-[color:var(--color-amber-base)]" />
            <span>ECE 14.09 Certified</span>
          </div>
          <div>RCD 015033319</div>
          <div>17 UK Installers</div>
        </motion.div>
      </div>
    </section>
  );
}
