import { motion } from 'framer-motion';
import { Search, Send, PhoneCall, Truck } from 'lucide-react';

const steps = [
  {
    num: '01',
    title: 'Browse & Choose',
    desc: 'Explore the range. Spec your build. Add to basket.',
    Icon: Search,
  },
  {
    num: '02',
    title: 'Send Enquiry',
    desc: 'Submit your basket with vehicle and fitment details.',
    Icon: Send,
  },
  {
    num: '03',
    title: 'We Call You',
    desc: 'Direct line to the workshop. Confirm and schedule.',
    Icon: PhoneCall,
  },
  {
    num: '04',
    title: 'Built & Delivered',
    desc: 'Precision-built to order. Delivered UK-wide.',
    Icon: Truck,
  },
];

export function HowItWorks() {
  return (
    <section className="relative overflow-hidden bg-[color:var(--color-ink-900)] py-24 md:py-32">
      <div className="absolute inset-0 bg-grid bg-grid-fade opacity-40" />

      <div className="relative mx-auto max-w-7xl px-4 md:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 text-center"
        >
          <div className="inline-flex items-center gap-3">
            <span className="h-px w-10 bg-[color:var(--color-amber-base)]" />
            <span className="text-xs font-black uppercase tracking-[0.2em] text-[color:var(--color-amber-base)]">
              The Process
            </span>
            <span className="h-px w-10 bg-[color:var(--color-amber-base)]" />
          </div>
          <h2 className="mt-4 font-black uppercase leading-[0.9] tracking-tightest text-white text-4xl md:text-6xl">
            Four steps. <span className="text-[color:var(--color-ink-400)]">Zero fuss.</span>
          </h2>
        </motion.div>

        {/* Stepper — horizontal desktop, vertical mobile */}
        <div className="relative">
          {/* Connecting line — desktop */}
          <div className="absolute left-0 right-0 top-12 hidden h-px bg-gradient-to-r from-transparent via-[color:var(--color-ink-600)] to-transparent md:block" />

          <div className="grid gap-12 md:grid-cols-4 md:gap-6">
            {steps.map((step, i) => {
              const Icon = step.Icon;
              return (
                <motion.div
                  key={step.num}
                  initial={{ opacity: 0, x: -30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, margin: '-80px' }}
                  transition={{
                    delay: i * 0.15,
                    duration: 0.6,
                    ease: [0.22, 1, 0.36, 1],
                  }}
                  className="relative flex gap-5 md:flex-col md:items-start md:gap-4"
                >
                  {/* Icon plate */}
                  <div className="relative z-10 flex h-24 w-24 shrink-0 items-center justify-center rounded-lg border border-[color:var(--color-ink-600)] bg-[color:var(--color-ink-800)] md:h-24 md:w-24">
                    <Icon className="h-8 w-8 text-[color:var(--color-amber-base)]" strokeWidth={1.8} />
                    <div className="absolute -right-2 -top-2 rounded-sm border border-[color:var(--color-amber-base)] bg-[color:var(--color-ink-900)] px-1.5 py-0.5 text-[10px] font-black text-[color:var(--color-amber-base)]">
                      {step.num}
                    </div>
                  </div>

                  {/* Copy */}
                  <div className="flex-1 pt-1 md:pt-4">
                    <h3 className="font-black uppercase tracking-tight text-white text-xl">
                      {step.title}
                    </h3>
                    <p className="mt-2 text-sm text-[color:var(--color-ink-300)]">
                      {step.desc}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
