import { Nav } from './components/Nav';
import { Hero } from './components/Hero';
import { TrustMarquee } from './components/TrustMarquee';
import { FeaturedProduct } from './components/FeaturedProduct';
import { ProductGrid } from './components/ProductGrid';
import { HowItWorks } from './components/HowItWorks';
import { WhyRoam } from './components/WhyRoam';
import { FAQ } from './components/FAQ';
import { Footer } from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-[color:var(--color-ink-900)] text-white antialiased">
      <Nav />
      <main>
        <Hero />
        <TrustMarquee />
        <FeaturedProduct />
        <ProductGrid />
        <HowItWorks />
        <WhyRoam />
        <FAQ />
      </main>
      <Footer />
    </div>
  );
}

export default App;
