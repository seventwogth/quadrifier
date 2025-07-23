use pyo3::prelude::*;
use pyo3::types::PyTuple;

#[pyfunction]
fn recalculate_quads(
    vertices: Vec<(f32, f32, f32)>,
    faces: Vec<Vec<usize>>,
) -> PyResult<(Vec<(f32, f32, f32)>, Vec<Vec<usize>>)> {
    println!("Called recalculate_quads (stub)");
    Ok((vertices, faces))
}

#[pymodule]
fn quadcore(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(recalculate_quads, m)?)?;
    Ok(())
}

