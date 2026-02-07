/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // 茶绿科幻配色方案 (Tea-Cyber Zen)
        tea: {
          // 主色调 - 茶绿色
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#2E8B57',    // 茶绿主色
          600: '#256f46',
          700: '#166534',
          800: '#14532d',
          900: '#052e16',

          // 亮色变体（发光效果）
          glow: '#4ade80',
          light: '#86efac',
        },
        cyber: {
          // 赛博蓝（科技感强调色）
          blue: '#00E5FF',
          blueDark: '#00b8d4',
          blueGlow: 'rgba(0, 229, 255, 0.5)',

          // 霓虹绿（成功状态）
          green: '#39FF14',
          greenDark: '#32cd32',

          // 浅色模式
          light: '#ffffff',
          lighter: '#f8fafc',
          lightGray: '#e2e8f0',
          text: '#1e293b',
          textSecondary: '#64748b',
          border: '#e2e8f0',

          // 深色模式
          dark: '#0a0f1a',
          darker: '#050810',
          darkGray: '#1a1f2e',
          darkBorder: '#2a3142',

          // 强调色
          primary: '#00E5FF',   // 赛博蓝
          secondary: '#2E8B57', // 茶绿
          accent: '#39FF14',   // 霓虹绿
          warning: '#f59e0b',   // 琥珀金
          danger: '#ef4444',    // 珊瑚红
        }
      },
      borderRadius: {
        // 圆润边角（茶道美学）
        'zen': '12px',
        'zen-sm': '8px',
        'zen-lg': '16px',
        'zen-xl': '24px',
        'zen-full': '9999px',
      },
      fontFamily: {
        // 使用衬线字体营造东方美学
        sans: ['Noto Serif SC', 'Inter', 'system-ui', 'sans-serif'],
        serif: ['Noto Serif SC', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'glow': 'glow 3s ease-in-out infinite alternate',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'slide-up': 'slideUp 0.5s ease-out forwards',
        'slide-down': 'slideDown 0.4s ease-out forwards',
        'fade-in': 'fadeIn 0.4s ease-out forwards',
        'scale-in': 'scaleIn 0.4s ease-out forwards',
        'spin-slow': 'spinSlow 4s linear infinite',
        'aurora': 'aurora 8s ease infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(46, 139, 87, 0.3), 0 0 20px rgba(46, 139, 87, 0.1)' },
          '100%': { boxShadow: '0 0 20px rgba(46, 139, 87, 0.5), 0 0 40px rgba(46, 139, 87, 0.2)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(46, 139, 87, 0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(46, 139, 87, 0.5)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        slideUp: {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95) translateY(10px)', opacity: '0' },
          '100%': { transform: 'scale(1) translateY(0)', opacity: '1' },
        },
        spinSlow: {
          'from': { transform: 'rotate(0deg)' },
          'to': { transform: 'rotate(360deg)' },
        },
        aurora: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      backgroundImage: {
        // 科技网格背景
        'grid-light': "linear-gradient(rgba(46, 139, 87, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(46, 139, 87, 0.03) 1px, transparent 1px)",
        'grid-dark': "linear-gradient(rgba(0, 229, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 229, 255, 0.05) 1px, transparent 1px)",

        // 渐变背景
        'gradient-tea': 'linear-gradient(135deg, #2E8B57 0%, #166534 100%)',
        'gradient-cyber': 'linear-gradient(135deg, #00E5FF 0%, #0066cc 100%)',
        'gradient-sunset': 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',

        // 发光渐变
        'glow-tea': 'linear-gradient(135deg, rgba(46, 139, 87, 0.1) 0%, rgba(0, 229, 255, 0.1) 100%)',
      },
      boxShadow: {
        // 茶绿发光阴影
        'tea-sm': '0 2px 8px rgba(46, 139, 87, 0.15)',
        'tea-md': '0 4px 16px rgba(46, 139, 87, 0.2)',
        'tea-lg': '0 8px 32px rgba(46, 139, 87, 0.25)',
        'tea-glow': '0 0 20px rgba(46, 139, 87, 0.4)',

        // 赛博发光阴影
        'cyber-sm': '0 2px 8px rgba(0, 229, 255, 0.15)',
        'cyber-md': '0 4px 16px rgba(0, 229, 255, 0.25)',
        'cyber-glow': '0 0 20px rgba(0, 229, 255, 0.4)',

        // 暗色科技阴影
        'dark-sm': '0 2px 8px rgba(0, 0, 0, 0.3)',
        'dark-md': '0 4px 16px rgba(0, 0, 0, 0.4)',
      },
      transitionDuration: {
        '400': '400ms',
      },
      transitionTimingFunction: {
        'bounce': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
    },
  },
  plugins: [],
}
