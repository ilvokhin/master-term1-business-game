function(doc) {
  if( doc.doc_type == "Task" && doc.project ) {
    emit(doc.project, doc);
  }
}
