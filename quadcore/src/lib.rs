use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::{HashMap, HashSet};

type Vertex = (f32, f32, f32);
type Face = Vec<usize>;

#[pyfunction]
fn recalculate_quads(
    vertices: Vec<Vertex>,
    faces: Vec<Face>,
) -> PyResult<(Vec<Vertex>, Vec<Face>)> {
    println!("Recalculating quads...");

    let mut new_faces: Vec<Face> = Vec::new();

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

#[pyfunction]
fn quad_fill_holes(
    vertices: Vec<Vertex>,
    faces: Vec<Face>,
) -> PyResult<(Vec<Vertex>, Vec<Face>)> {
    println!("Running quad grid fill...");

    let mut edge_map: HashMap<(usize, usize), usize> = HashMap::new();

    for face in &faces {
        for i in 0..face.len() {
            let a = face[i];
            let b = face[(i + 1) % face.len()];
            let key = if a < b { (a, b) } else { (b, a) };
            *edge_map.entry(key).or_insert(0) += 1;
        }
    }

    let mut boundary_edges: Vec<(usize, usize)> = edge_map
        .iter()
        .filter_map(|(&(a, b), &count)| if count == 1 { Some((a, b)) } else { None })
        .collect();

    let mut edge_loops: Vec<Vec<usize>> = Vec::new();
    let mut visited: HashSet<(usize, usize)> = HashSet::new();

    while let Some((start, end)) = boundary_edges.pop() {
        if visited.contains(&(start, end)) || visited.contains(&(end, start)) {
            continue;
        }

        let mut loop_vertices = vec![start, end];
        visited.insert((start, end));

        let mut current = end;
        loop {
            let next_edge = boundary_edges
                .iter()
                .find(|&&(a, b)| a == current || b == current)
                .copied();

            if let Some((a, b)) = next_edge {
                let next = if a == current { b } else { a };
                if next == start {
                    break;
                }
                loop_vertices.push(next);
                visited.insert((a, b));
                boundary_edges.retain(|&e| e != (a, b) && e != (b, a));
                current = next;
            } else {
                break;
            }
        }

        if loop_vertices.len() >= 3 {
            edge_loops.push(loop_vertices);
        }
    }

    let mut new_faces = faces.clone();

    for loop_vertices in edge_loops {
        let len = loop_vertices.len();
        let even = len % 2 == 0;
        for i in (0..len).step_by(2) {
            let i0 = loop_vertices[i % len];
            let i1 = loop_vertices[(i + 1) % len];
            let i2 = loop_vertices[(i + 2) % len];
            let i3 = loop_vertices[(i + 3) % len];
            new_faces.push(vec![i0, i1, i2, i3]);
            if !even && i + 4 >= len {
                break;
            }
        }
    }

    Ok((vertices, new_faces))
}

#[pymodule]
fn quadcore(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(recalculate_quads, m)?)?;
    m.add_function(wrap_pyfunction!(quad_fill_holes, m)?)?;
    Ok(())
}

