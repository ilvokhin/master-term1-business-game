function(doc) {
  if( doc.doc_type == "Task" && doc.author ) {
    emit(doc.author, doc);
  }
}
