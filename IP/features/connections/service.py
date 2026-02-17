"""Connection graph service helpers."""

from __future__ import annotations

from typing import Tuple


def verify_all_connections(project_root: str, files_df) -> Tuple:
    """
    Verify import connections for all files in a DataFrame.

    Returns:
        Tuple of (files_df with status updates, connection_results dict)
    """
    from IP.connection_verifier import ConnectionVerifier

    verifier = ConnectionVerifier(project_root)
    connection_results = {}

    for _, row in files_df.iterrows():
        file_path = row["path"]
        result = verifier.verify_file(file_path)
        connection_results[file_path] = result

    return files_df, connection_results


def build_connection_graph(project_root: str):
    """
    Convenience function to build a complete connection graph.

    Usage:
        graph = build_connection_graph("/path/to/project")
        print(graph.to_json())
    """
    from IP.connection_verifier import ConnectionGraph, ConnectionVerifier

    verifier = ConnectionVerifier(project_root)
    results = verifier.verify_project()

    graph = ConnectionGraph(verifier)
    graph.build_from_results(results)
    graph.detect_cycles()
    graph.calculate_centrality()
    graph.calculate_depth()

    return graph

