"""📐 Que se puede medir de UNA muestra cruda, sin mirar el resto del dataset.

Trabaja sobre `Muestra`, la base comun: sirve igual para una sena aislada y
para una frase (LSP). No conoce umbrales ni criterios de calidad — solo mide.
Quien juzga es `diagnostico_del_dataset`.
"""

from __future__ import annotations

from dataclasses import dataclass

from ...dominio.entidades import Lado, Muestra

#: Orden canonico de las manos, el mismo que las ranuras del tensor.
RANURAS: tuple[Lado, ...] = Lado.canonicos()


@dataclass(frozen=True, slots=True)
class MetricasDeMuestra:
    """Lo medible de una muestra: cuanto dura y cuanta mano hay dentro."""

    n_frames: int
    frames_con_alguna_mano: int
    frames_con_las_dos_manos: int
    frames_por_lado: tuple[int, ...]
    segundos: float | None

    @property
    def frames_sin_manos(self) -> int:
        """Frames en los que MediaPipe no encontro ninguna mano."""
        return self.n_frames - self.frames_con_alguna_mano

    @property
    def proporcion_con_mano(self) -> float:
        """Fraccion de la grabacion con al menos una mano detectada."""
        return self.frames_con_alguna_mano / self.n_frames

    @property
    def usa_las_dos_manos(self) -> bool:
        """¿Es una sena bimanual? Se responde por la mayoria de los frames.

        Un frame aislado con dos manos puede ser la otra mano pasando por el
        encuadre; la mitad de la grabacion ya es intencion.
        """
        return self.frames_con_las_dos_manos * 2 >= self.n_frames


def medir(muestra: Muestra) -> MetricasDeMuestra:
    """Recorre los frames una sola vez y devuelve todas las metricas."""
    con_alguna = 0
    con_las_dos = 0
    por_lado = [0] * len(RANURAS)

    for frame in muestra.frames:
        # `Frame.mano()` ya resuelve el duplicado de lado de MediaPipe
        presentes = [frame.mano(lado) is not None for lado in RANURAS]
        cuantas = sum(presentes)
        if cuantas:
            con_alguna += 1
        if cuantas == len(RANURAS):
            con_las_dos += 1
        for ranura, presente in enumerate(presentes):
            por_lado[ranura] += int(presente)

    return MetricasDeMuestra(
        n_frames=muestra.n_frames,
        frames_con_alguna_mano=con_alguna,
        frames_con_las_dos_manos=con_las_dos,
        frames_por_lado=tuple(por_lado),
        segundos=_segundos(muestra),
    )


def _segundos(muestra: Muestra) -> float | None:
    """Duracion real, o `None` si la grabacion no reporto fps."""
    if not muestra.fps_aprox:
        return None
    return muestra.n_frames / muestra.fps_aprox
