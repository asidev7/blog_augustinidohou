/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html', './static/**/*.js'],
  theme: {
    extend: {
      colors: {
        primary:   '#2563EB',
        secondary: '#0048AE',
        accent:    '#38BDF8',
        surface:   '#111118',
        border:    '#1E1E28',
        light:     '#E2E8F0',
        muted:     '#64748B',
        success:   '#22C55E',
        dark:      '#0A0A0F',
      },
      fontFamily: {
        display: ['Sora', 'sans-serif'],
        body:    ['Inter', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'float':    'float 6s ease-in-out infinite',
        'glow':     'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.6s ease forwards',
        'fade-in':  'fadeIn 0.8s ease forwards',
        'blink':    'blink 1s step-end infinite',
      },
      keyframes: {
        float:   { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-18px)' } },
        glow:    { from: { boxShadow: '0 0 10px #2563EB' }, to: { boxShadow: '0 0 25px #38BDF8, 0 0 50px #2563EB' } },
        slideUp: { from: { opacity: 0, transform: 'translateY(30px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
        fadeIn:  { from: { opacity: 0 }, to: { opacity: 1 } },
        blink:   { '50%': { opacity: 0 } },
      },
      backgroundImage: {
        'gradient-tech': 'linear-gradient(135deg, #2563EB 0%, #0048AE 60%, #0A0A0F 100%)',
        'gradient-card': 'linear-gradient(180deg, #111118 0%, #0A0A0F 100%)',
        'dot-grid': 'radial-gradient(circle, #1E1E28 1px, transparent 1px)',
      },
    },
  },
  plugins: [require('@tailwindcss/typography'), require('@tailwindcss/forms')],
}
