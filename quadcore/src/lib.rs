use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn recalculate_quads(
    vertices: Vec<(f32, f32, f32)>,
    faces: Vec<Vec<usize>>,
) -> PyResult<(Vec<(f32, f32, f32)>, Vec<Vec<usize>>)> {
    println!("Recalculating quads...");

    let mut new_faces: Vec<Vec<usize>> = Vec::new();

    for face in faces {
        if face.len() < 3 {
            continue;
        }

        let mut chunk = Vec::new();
        for idx in face {
            chunk.push(idx);
            if chunk.len() == 4 {
                new_faces.push(chunk.clone());
                chunk.clear();
            }
        }

        if !chunk.is_empty() {
            while chunk.len() < 4 {
                let last = *chunk.last().unwrap();
                chunk.push(last);
            }
            new_faces.push(chunk);
        }
    }

    Ok((vertices, new_faces))
}

#[pymodule]
fn quadcore(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(recalculate_quads, m)?)?;
    Ok(())
}

