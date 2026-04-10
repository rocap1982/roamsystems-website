const footerLinks = {
  Products: ['Frames', 'Upholstery', 'Kitchens', 'Storage', 'Panels'],
  Support: ['Installers', 'Delivery', 'Warranty', 'Contact', 'FAQ'],
  Legal: ['Privacy', 'Terms', 'Cookies', 'Returns', 'Shipping'],
};

export function Footer() {
  return (
    <footer className="relative border-t border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-950)] py-16 md:py-20">
      <div className="mx-auto max-w-7xl px-4 md:px-8">
        <div className="grid gap-12 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
          {/* Brand column */}
          <div>
            <img
              src="/images/roam-systems-logo.png"
              alt="ROAM Systems"
              className="h-28 w-auto md:h-32"
            />
            <p className="mt-6 max-w-sm text-sm text-[color:var(--color-ink-300)]">
              Precision-engineered campervan furniture.<br />
              Made in the UK.
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              <div className="rounded-sm border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] px-3 py-1.5 text-[10px] font-bold uppercase tracking-widest text-[color:var(--color-ink-200)]">
                ECE 14.09
              </div>
              <div className="rounded-sm border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] px-3 py-1.5 text-[10px] font-bold uppercase tracking-widest text-[color:var(--color-ink-200)]">
                RCD 015033319
              </div>
              <div className="rounded-sm border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] px-3 py-1.5 text-[10px] font-bold uppercase tracking-widest text-[color:var(--color-ink-200)]">
                M1 Certified
              </div>
            </div>
          </div>

          {/* Link columns */}
          {Object.entries(footerLinks).map(([group, links]) => (
            <div key={group}>
              <div className="flex items-center gap-3">
                <span className="h-px w-6 bg-[color:var(--color-amber-base)]" />
                <h4 className="text-xs font-black uppercase tracking-[0.2em] text-[color:var(--color-amber-base)]">
                  {group}
                </h4>
              </div>
              <ul className="mt-5 space-y-3">
                {links.map((link) => (
                  <li key={link}>
                    <a
                      href={`#${link.toLowerCase()}`}
                      className="text-sm font-semibold uppercase tracking-wider text-[color:var(--color-ink-200)] transition-colors hover:text-[color:var(--color-amber-base)]"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="mt-16 flex flex-col items-start justify-between gap-4 border-t border-[color:var(--color-ink-600)] pt-8 md:flex-row md:items-center">
          <p className="text-xs uppercase tracking-wider text-[color:var(--color-ink-400)]">
            © 2025 ROAM Systems. Manufactured by Romark Engineering Ltd, Essex.
          </p>
          <p className="text-xs uppercase tracking-wider text-[color:var(--color-ink-400)]">
            Built in the UK. Delivered worldwide... one day.
          </p>
        </div>
      </div>
    </footer>
  );
}
