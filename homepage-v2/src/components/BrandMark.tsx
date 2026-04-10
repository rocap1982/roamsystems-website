import { motion } from 'framer-motion';

type Size = 'sm' | 'md' | 'lg';

const sizeMap: Record<Size, { logo: string; pad: string; bracket: string }> = {
  sm: { logo: 'h-14 md:h-16', pad: '-m-3', bracket: '-inset-2' },
  md: { logo: 'h-20 md:h-24', pad: '-m-4', bracket: '-inset-2.5' },
  lg: { logo: 'h-28 md:h-32', pad: '-m-6', bracket: '-inset-3' },
};

/**
 * BrandMark — industrial treatment around the ROAM Systems logo.
 *
 * Layers (back to front):
 *  1. Ambient amber radial glow (always on, intensifies on hover)
 *  2. Slow-rotating conic aura (masked to a ring)
 *  3. Precision corner brackets (permanent, amber)
 *  4. The real logo PNG
 *  5. Diagonal scan-line sweep on hover
 *
 * All motion respects prefers-reduced-motion via the global CSS override.
 */
export function BrandMark({ size = 'md' }: { size?: Size }) {
  const s = sizeMap[size];

  return (
    <motion.span
      initial={{ opacity: 0, scale: 0.92 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
      className="group relative inline-flex items-center justify-center"
    >
      {/* Ambient amber halo — always on, brighter on hover */}
      <span
        aria-hidden
        className={`pointer-events-none absolute ${s.pad} rounded-full bg-[radial-gradient(circle,var(--color-amber-base)_0%,transparent_65%)] opacity-20 blur-2xl transition-opacity duration-500 group-hover:opacity-60`}
      />

      {/* Slow-rotating conic aura ring */}
      <motion.span
        aria-hidden
        animate={{ rotate: 360 }}
        transition={{ duration: 36, repeat: Infinity, ease: 'linear' }}
        className={`pointer-events-none absolute ${s.pad} rounded-full opacity-50`}
        style={{
          background:
            'conic-gradient(from 0deg, transparent 0deg, var(--color-amber-base) 30deg, transparent 90deg, transparent 180deg, var(--color-amber-base) 210deg, transparent 270deg)',
          WebkitMask:
            'radial-gradient(circle, transparent 46%, black 48%, black 52%, transparent 54%)',
          mask:
            'radial-gradient(circle, transparent 46%, black 48%, black 52%, transparent 54%)',
        }}
      />

      {/* Precision corner brackets */}
      <span
        aria-hidden
        className={`pointer-events-none absolute ${s.bracket} z-20`}
      >
        <span className="absolute left-0 top-0 h-3 w-3 border-l-2 border-t-2 border-[color:var(--color-amber-base)] transition-all duration-300 group-hover:h-4 group-hover:w-4" />
        <span className="absolute right-0 top-0 h-3 w-3 border-r-2 border-t-2 border-[color:var(--color-amber-base)] transition-all duration-300 group-hover:h-4 group-hover:w-4" />
        <span className="absolute bottom-0 left-0 h-3 w-3 border-b-2 border-l-2 border-[color:var(--color-amber-base)] transition-all duration-300 group-hover:h-4 group-hover:w-4" />
        <span className="absolute bottom-0 right-0 h-3 w-3 border-b-2 border-r-2 border-[color:var(--color-amber-base)] transition-all duration-300 group-hover:h-4 group-hover:w-4" />
      </span>

      {/* The actual logo */}
      <motion.img
        src="/images/roam-systems-logo.png"
        alt="ROAM Systems"
        className={`${s.logo} relative z-10 w-auto drop-shadow-[0_0_20px_rgba(232,126,4,0.25)] transition-transform duration-500 group-hover:scale-[1.03]`}
        loading="eager"
        whileHover={{
          filter: 'drop-shadow(0 0 30px rgba(232,126,4,0.55))',
        }}
      />

      {/* Scan-line sweep on hover */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 z-30 overflow-hidden"
      >
        <span className="brand-scan absolute left-0 right-0 h-px bg-gradient-to-r from-transparent via-[color:var(--color-amber-base)] to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
      </span>
    </motion.span>
  );
}
