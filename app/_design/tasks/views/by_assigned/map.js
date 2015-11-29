function(doc) {
  if( doc.doc_type == "Task" && doc.assigned ) {
    emit(doc.assigned, doc);
  }
}
