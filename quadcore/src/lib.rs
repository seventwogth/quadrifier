use pyo3::prelude::*;

#[pyfunction]
fn recalculate_mesh(py: Python, mesh: PyObject) -> PyResult<()> {
    println!("Called recalculate_mesh (stub)");
    Ok(())
}

#[pymodule]
fn rustlib(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(recalculate_mesh, m)?)?;
    Ok(())
}


