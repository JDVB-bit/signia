import { useState } from 'react'

function Button({children, variant = "default", onClick}){
    const styles = {
        // Usan el color "inverso" (el de la paleta contraria al tema activo)
        // para que resalten sin importar si el sitio esta en claro u oscuro.
        primary: 'rounded-md bg-brand-inverso px-5 py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90',
        secondary: 'rounded-md bg-secondary-inverso px-5 py-2.5 text-sm font-semibold text-slate-900 transition-opacity hover:opacity-90',
        sidebar: '',
        burble: '',
        stop: '',
        default: ''
    }
    
    return (
        <button className={styles[variant]} onClick={onClick}>
            {variant === 'sidebar' ? (
                <span className=''></span>
            ) : (
                children
            )}
        </button>
    )
}

export default Button