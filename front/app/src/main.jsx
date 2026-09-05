import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import AppRoot from './AppRoot.jsx'
import { aplicarTemaInicial } from './utils/theme.js'

// Se aplica el tema (claro/oscuro) antes de renderizar nada, para que la
// pantalla de carga y el resto de la app nazcan ya con los colores
// correctos, sin parpadeos.
aplicarTemaInicial()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <AppRoot />
    </BrowserRouter>
  </StrictMode>,
)
