import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import AplicacionRaiz from './presentacion/AplicacionRaiz.jsx'
import './presentacion/estilos/animaciones.css'
import { aplicarTemaInicial } from './infra/navegador/preferenciaDeTema.js'

// Se aplica el tema (claro/oscuro) antes de renderizar nada, para que la
// pantalla de carga y el resto de la app nazcan ya con los colores
// correctos, sin parpadeos.
aplicarTemaInicial()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <AplicacionRaiz />
    </BrowserRouter>
  </StrictMode>,
)
