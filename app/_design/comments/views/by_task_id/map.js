function(doc) {
  if( doc.doc_type == "Comment" && doc.task_id ) {
    emit(doc.task_id, doc);
  }
}
