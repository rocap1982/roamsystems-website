import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Plus } from 'lucide-react';

const faqs = [
  { q: 'What is M1 Certification?', a: 'M1 certification (ECE Regulation 14.09) is the European safety standard for seats and their anchorages in motor vehicles. On our U-shape frame, the certification covers the rear travel seat with its integrated 3-point seatbelts and ISOFIX anchor points, which is independently crash tested — not the full frame as a system. Side bench sections are for stationary use only.' },
  { q: 'Will ROAM furniture fit my campervan?', a: 'Our system is designed around the VW Transporter T5/T6/T6.1, Ford Transit Custom (2012+), Renault Trafic and Nissan Primastar. SWB and LWB configurations available. If you are unsure about compatibility, send us your vehicle details and we will confirm fitment.' },
  { q: 'Can I customise my order?', a: '100+ fabric options across the upholstery range, plus configuration choices across frames, kitchens and storage. Bespoke layouts can be accommodated — contact us with your requirements.' },
  { q: 'Do I need professional installation?', a: 'The M1 certified frame is best fitted by an approved installer to keep certification valid. Storage, kitchens and panels are designed for straightforward self-fit with basic tools.' },
  { q: 'How long does delivery take?', a: 'Current production lead time: typically 2-4 weeks from order confirmation. UK delivery is 3–5 working days from dispatch.' },
  { q: 'Do you offer a warranty?', a: 'Yes — all ROAM products come with a manufacturer warranty. Full terms are supplied with your order.' },
  { q: 'How do I place an order?', a: 'Add items to your basket and send an enquiry. We will call you to confirm spec, lead time and arrange payment — no surprise checkouts.' },
  { q: 'Do you deliver internationally?', a: 'Currently we deliver UK-wide only. For international enquiries, contact us directly and we can discuss options.' },
];

function FAQItem({ item, isOpen, onToggle }: { item: typeof faqs[number]; isOpen: boolean; onToggle: () => void }) {
  return (
    <div className="border-b border-[color:var(--color-ink-600)] last:border-b-0">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={isOpen}
        className="group flex w-full items-center justify-between gap-6 py-6 text-left transition-colors hover:text-[color:var(--color-amber-base)]"
      >
        <span className="font-black uppercase tracking-tight text-white text-lg md:text-xl">{item.q}</span>
        <motion.div
          animate={{ rotate: isOpen ? 45 : 0 }}
          transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] transition-colors group-hover:border-[color:var(--color-amber-base)]"
        >
          <Plus className="h-4 w-4 text-[color:var(--color-amber-base)]" strokeWidth={3} />
        </motion.div>
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            key="content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ height: { duration: 0.4, ease: [0.22, 1, 0.36, 1] }, opacity: { duration: 0.25 } }}
            className="overflow-hidden"
          >
            <p className="pb-6 pr-16 text-[color:var(--color-ink-300)]">{item.a}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);
  return (
    <section id="faq" className="relative bg-[color:var(--color-ink-900)] py-24 md:py-32">
      <div className="mx-auto max-w-4xl px-4 md:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-12 text-center"
        >
          <div className="inline-flex items-center gap-3">
            <span className="h-px w-10 bg-[color:var(--color-amber-base)]" />
            <span className="text-xs font-black uppercase tracking-[0.2em] text-[color:var(--color-amber-base)]">FAQ</span>
            <span className="h-px w-10 bg-[color:var(--color-amber-base)]" />
          </div>
          <h2 className="mt-4 font-black uppercase leading-[0.9] tracking-tightest text-white text-4xl md:text-6xl">
            Questions. <span className="text-[color:var(--color-ink-400)]">Answered.</span>
          </h2>
        </motion.div>

        <div className="rounded-2xl border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] px-6 md:px-10">
          {faqs.map((item, i) => (
            <FAQItem
              key={item.q}
              item={item}
              isOpen={openIndex === i}
              onToggle={() => setOpenIndex(openIndex === i ? null : i)}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
