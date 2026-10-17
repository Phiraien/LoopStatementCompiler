{
  int outer = 2;
  do {
    int inner = 3;
    while (inner > 0) {
      {
        outer = outer + inner;
      }
      inner = inner - 1;
    }
    outer = outer - 1;
  } while (outer > 0);
}
