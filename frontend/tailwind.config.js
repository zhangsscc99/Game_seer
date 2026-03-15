/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1a1f3a',
          dark: '#0d1028',
          light: '#252d52'
        },
        accent: {
          DEFAULT: '#f0c040',
          dark: '#c9a030',
          light: '#f5d060'
        },
        rare: {
          DEFAULT: '#4080ff',
          dark: '#2060dd',
          light: '#60a0ff'
        },
        sr: {
          DEFAULT: '#ffa500',
          dark: '#cc8400',
          light: '#ffbb33'
        },
        ssr: {
          DEFAULT: '#ff4500',
          dark: '#cc3700',
          light: '#ff6633'
        },
        ur: {
          DEFAULT: '#9b30ff',
          dark: '#7a20dd',
          light: '#b550ff'
        },
        space: {
          900: '#0d0f1e',
          800: '#111428',
          700: '#161b35',
          600: '#1a1f3a',
          500: '#252d52',
          400: '#2e3a6e'
        }
      },
      boxShadow: {
        'glow-accent': '0 0 15px rgba(240, 192, 64, 0.5)',
        'glow-rare': '0 0 15px rgba(64, 128, 255, 0.5)',
        'glow-sr': '0 0 15px rgba(255, 165, 0, 0.5)',
        'glow-ssr': '0 0 15px rgba(255, 69, 0, 0.5)',
        'glow-ur': '0 0 15px rgba(155, 48, 255, 0.5)',
        'glow-white': '0 0 15px rgba(255, 255, 255, 0.3)'
      },
      fontFamily: {
        game: ['"Noto Sans SC"', 'sans-serif']
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'float': 'float 3s ease-in-out infinite'
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' }
        }
      }
    }
  },
  plugins: []
}
