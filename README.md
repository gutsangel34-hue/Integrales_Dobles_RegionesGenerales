# Simulación: valor promedio de f(x, y) = xy sobre un triángulo

Simulación en Python para la exposición de **Cálculo Vectorial** (Universidad de La Salle), tema 5: *Integrales dobles en regiones generales* (Stewart, Sec. 15.2, ejercicio 61).

**Problema:** sea f(x, y) = xy y D el triángulo con vértices (0, 0), (1, 0) y (1, 3). Hallar el valor promedio de f en D.

| Cantidad | Valor |
|---|---|
| Área de D | 3/2 |
| Integral doble de xy sobre D | 9/8 |
| Valor promedio f_prom | 3/4 |

## Qué hace el código

El archivo `simulacion_valor_promedio.py` hace todo en una sola ejecución:

1. **Verifica el resultado** con `sympy`: calcula el área, la integral doble y el valor promedio, y comprueba que el otro orden de integración (tipo II) da lo mismo.
2. **Genera una simulación 3D interactiva** (`simulacion_valor_promedio.html`) con:
   - la región D sombreada en el plano xy;
   - la superficie z = xy sobre D;
   - el plano z = h con un **deslizador**: el título muestra la integral de (xy − h) sobre D, que vale 9/8 − (3/2)h y se anula justo en h = 3/4, el valor promedio.
3. **Genera una imagen estática** (`simulacion_valor_promedio.png`) para usar en las diapositivas.

## Librerías necesarias

- Python 3.9 o superior
- `numpy`
- `sympy`
- `plotly`
- `matplotlib`

Se instalan todas con un solo comando:

```bash
pip install numpy sympy plotly matplotlib
```

## Cómo ejecutarlo en VS Code

Solo necesitas descargar **`simulacion_valor_promedio.py`**; el HTML y el PNG los crea el propio código.

1. Descarga `simulacion_valor_promedio.py` y guárdalo en una carpeta.
2. Abre esa carpeta en **Visual Studio Code** (con la extensión de Python instalada).
3. Abre la **Terminal** de VS Code (menú *Terminal → Nueva terminal*) e instala las librerías:

   ```bash
   pip install numpy sympy plotly matplotlib
   ```

4. Ejecuta el archivo, con el botón ▶ de VS Code o desde la terminal:

   ```bash
   python simulacion_valor_promedio.py
   ```

5. En la terminal debe aparecer:

   ```
   A(D) = 3/2,  integral doble de xy sobre D = 9/8,  f_prom = 3/4
   Listo: simulacion_valor_promedio.html y .png
   ```

6. En la misma carpeta se habrán creado dos archivos. Abre **`simulacion_valor_promedio.html`** con doble clic (se ve en cualquier navegador, sin internet) y mueve el deslizador.

## Solución de problemas

- **`ModuleNotFoundError: No module named 'plotly'`** (o `sympy`, `numpy`, `matplotlib`): falta instalar las librerías; repite el paso 3.
- **`pip` no se reconoce:** prueba con `python -m pip install numpy sympy plotly matplotlib`.
- **Error de codificación en la consola de Windows:** ejecuta `python -X utf8 simulacion_valor_promedio.py`.

## Autor

Angel Vásquez Sequeda
