import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, ShoppingBag } from 'lucide-react';
import { BrandMark } from './BrandMark';
import { navLinks, navLinksSecondary } from './homeData';

export function Nav() {
  const [open, setOpen] = useState(false);
  const [cartCount, setCartCount] = useState(0);

  // Sync cart count from the existing localStorage-backed cart
  useEffect(() => {
    const read = () => {
      try {
        const items = JSON.parse(localStorage.getItem('roam-cart') || '[]');
        const count = items.reduce((s: number, it: { qty: number }) => s + (it.qty || 0), 0);
        setCartCount(count);
      } catch {
        setCartCount(0);
      }
    };
    read();
    const id = window.setInterval(read, 500);
    window.addEventListener('storage', read);
    return () => {
      window.clearInterval(id);
      window.removeEventListener('storage', read);
    };
  }, []);

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  const openCart = () => {
    document.getElementById('cart-sidebar')?.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  };

  return (
    <>
      <motion.header
        initial={{ y: -24, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="fixed inset-x-0 top-0 z-50 border-b border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-900)]/92 backdrop-blur-xl"
      >
        <nav className="mx-auto flex h-24 max-w-[90rem] items-center justify-between gap-6 px-4 md:h-28 md:px-8">
          <a href="/" className="flex shrink-0 items-center" aria-label="ROAM Systems home">
            <BrandMark size="md" />
          </a>

          <ul className="hidden items-center gap-5 xl:gap-7 lg:flex">
            {navLinks.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  className="relative whitespace-nowrap text-[11px] font-semibold uppercase tracking-[0.15em] text-[color:var(--color-ink-200)] transition-colors hover:text-white xl:text-xs"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>

          <div className="flex shrink-0 items-center gap-3">
            <button
              type="button"
              onClick={openCart}
              aria-label={`Open cart (${cartCount} items)`}
              className="relative inline-flex h-10 w-10 items-center justify-center rounded-md border border-[color:var(--color-ink-600)] text-white transition-colors hover:border-[color:var(--color-amber-base)] hover:text-[color:var(--color-amber-base)]"
            >
              <ShoppingBag className="h-5 w-5" />
              {cartCount > 0 && (
                <span className="absolute -right-1.5 -top-1.5 flex h-5 min-w-5 items-center justify-center rounded-full bg-[color:var(--color-amber-base)] px-1 text-[10px] font-black text-black">
                  {cartCount}
                </span>
              )}
            </button>
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
                {[...navLinks, ...navLinksSecondary].map((link, i) => (
                  <motion.li
                    key={link.label}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 + i * 0.04, duration: 0.3 }}
                  >
                    <a
                      href={link.href}
                      onClick={() => setOpen(false)}
                      className="flex items-center justify-between rounded-md border border-transparent px-4 py-3.5 text-lg font-black uppercase tracking-tight text-white transition-all hover:border-[color:var(--color-ink-600)] hover:bg-[color:var(--color-ink-800)] hover:text-[color:var(--color-amber-base)]"
                    >
                      {link.label}
                      <span className="text-[color:var(--color-amber-base)]">→</span>
                    </a>
                  </motion.li>
                ))}
              </ul>
              <div className="border-t border-[color:var(--color-ink-600)] p-5">
                <a
                  href="/products"
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
