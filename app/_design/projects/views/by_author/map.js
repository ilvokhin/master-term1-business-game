function(doc) {
  if( doc.doc_type == "Project" && doc.author ) {
    emit(doc.author, doc);
  }
}
