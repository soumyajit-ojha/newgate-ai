import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// export default defineConfig({
//   plugins: [
//     react({
//       babel: {
//         plugins: [['babel-plugin-react-compiler']],
//       },
//     }),
//   ],
// })

export default defineConfig({
  plugins: [react()],
  server: {
    // This allows the backend to be on port 8000 and frontend on 5173
    host: true,
    headers: {
      // ⚠️ THIS FIXES THE GOOGLE POPUP ERROR
      "Cross-Origin-Opener-Policy": "same-origin-allow-popups",
      // "Cross-Origin-Embedder-Policy": "require-corp",
    },
    // Optional: This sets up a "Proxy" to fix Network Errors permanently
    // proxy: {
    //   '/api': {
    //     target: 'http://127.0.0.1:8000',
    //     changeOrigin: true,
    //     secure: false,
    //   }
    // }
  },
})
