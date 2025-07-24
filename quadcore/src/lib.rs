
use pyo3::prelude::*;

#[pyfunction]
fn recalculate_quads(
    vertices: Vec<(f32, f32, f32)>,
    faces: Vec<Vec<usize>>,
) -> PyResult<(Vec<(f32, f32, f32)>, Vec<Vec<usize>>)> {
    println!("Recalculating quads...");

    let mut new_faces = Vec::new();

    for face in faces {
        match face.len() {
            4 => {
                new_faces.push(face);
            }
            3 => {
                let mut quad = face.clone();
                quad.push(quad[2]);
                new_faces.push(quad);
            }
            n if n > 4 => {
                for i in 1..(face.len() - 2) {
                    let quad = vec![face[0], face[i], face[i + 1], face[i + 2]];
                    new_faces.push(quad);
                }
            }
            _ => {
            }
        }
    }
    Ok((vertices, new_faces))
}

#[pymodule]
fn quadcore(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(recalculate_quads, m)?)?;
    Ok(())
}


