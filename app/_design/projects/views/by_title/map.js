function(doc) {
  if( doc.doc_type == "Project" && doc.title ) {
    emit(doc.title, doc);
  }
}
