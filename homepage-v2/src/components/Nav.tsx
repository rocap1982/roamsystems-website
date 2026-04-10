import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, ShoppingBag } from 'lucide-react';
import { cn } from '../lib/utils';
import { BrandMark } from './BrandMark';

const NAV_LINKS = [
  { label: 'Frames', href: '#frames' },
  { label: 'Upholstery', href: '#upholstery' },
  { label: 'Kitchens', href: '#kitchens' },
  { label: 'Vehicles', href: '#vehicles' },
  { label: 'Installers', href: '#installers' },
  { label: 'Gallery', href: '#gallery' },
  { label: 'Contact', href: '#contact' },
];

export function Nav() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Lock body scroll when drawer open
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  return (
    <>
      <motion.header
        initial={{ y: -24, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className={cn(
          'fixed inset-x-0 top-0 z-50 transition-all duration-300',
          scrolled
            ? 'backdrop-blur-xl bg-[color:var(--color-ink-900)]/85 border-b border-[color:var(--color-ink-600)]'
            : 'bg-transparent border-b border-transparent'
        )}
      >
        <nav className="mx-auto flex h-24 max-w-7xl items-center justify-between px-4 md:h-28 md:px-8">
          {/* Logo */}
          <a href="#top" className="flex items-center" aria-label="ROAM Systems home">
            <BrandMark size="md" />
          </a>

          {/* Desktop links */}
          <ul className="hidden items-center gap-8 lg:flex">
            {NAV_LINKS.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  className="relative text-sm font-semibold uppercase tracking-wider text-[color:var(--color-ink-200)] transition-colors hover:text-white"
                >
                  {link.label}
                  <span className="absolute -bottom-1 left-0 h-px w-0 bg-[color:var(--color-amber-base)] transition-all duration-300 hover:w-full" />
                </a>
              </li>
            ))}
          </ul>

          {/* CTA + mobile trigger */}
          <div className="flex items-center gap-3">
            <a
              href="#products"
              className="hidden items-center gap-2 rounded-md bg-[color:var(--color-amber-base)] px-5 py-2.5 text-sm font-black uppercase tracking-wider text-black transition-all hover:bg-[color:var(--color-amber-bright)] hover:shadow-[0_0_30px_var(--color-amber-glow)] md:inline-flex"
            >
              <ShoppingBag className="h-4 w-4" strokeWidth={2.5} />
              Shop Now
            </a>
            <button
              type="button"
              onClick={() => setOpen(true)}
              aria-label="Open menu"
              className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-[color:var(--color-ink-600)] text-white transition-colors hover:border-[color:var(--color-amber-base)] hover:text-[color:var(--color-amber-base)] lg:hidden"
            >
              <Menu className="h-5 w-5" />
            </button>
          </div>
        </nav>
      </motion.header>

      {/* Mobile drawer */}
      <AnimatePresence>
        {open && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25 }}
              onClick={() => setOpen(false)}
              className="fixed inset-0 z-[60] bg-black/70 backdrop-blur-sm"
            />
            <motion.aside
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              className="fixed inset-y-0 right-0 z-[70] flex w-[min(88vw,360px)] flex-col border-l border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-900)]"
            >
              <div className="flex h-24 items-center justify-between border-b border-[color:var(--color-ink-600)] px-5 md:h-28">
                <BrandMark size="sm" />
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  aria-label="Close menu"
                  className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-[color:var(--color-ink-600)] text-white transition-colors hover:border-[color:var(--color-amber-base)] hover:text-[color:var(--color-amber-base)]"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <ul className="flex-1 space-y-1 overflow-y-auto p-5">
                {NAV_LINKS.map((link, i) => (
                  <motion.li
                    key={link.label}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 + i * 0.05, duration: 0.3 }}
                  >
                    <a
                      href={link.href}
                      onClick={() => setOpen(false)}
                      className="flex items-center justify-between rounded-md border border-transparent px-4 py-4 text-xl font-black uppercase tracking-tight text-white transition-all hover:border-[color:var(--color-ink-600)] hover:bg-[color:var(--color-ink-800)] hover:text-[color:var(--color-amber-base)]"
                    >
                      {link.label}
                      <span className="text-[color:var(--color-amber-base)]">→</span>
                    </a>
                  </motion.li>
                ))}
              </ul>
              <div className="border-t border-[color:var(--color-ink-600)] p-5">
                <a
                  href="#products"
                  onClick={() => setOpen(false)}
                  className="flex w-full items-center justify-center gap-2 rounded-md bg-[color:var(--color-amber-base)] px-5 py-4 text-sm font-black uppercase tracking-wider text-black transition-colors hover:bg-[color:var(--color-amber-bright)]"
                >
                  <ShoppingBag className="h-4 w-4" strokeWidth={2.5} />
                  Shop Now
                </a>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
