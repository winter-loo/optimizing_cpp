#if FUNC == 1
// unoptimized version
void Func(int a[], int &r) {
  int i;
  for (i = 0; i < 100; i++) {
    a[i] = r + i / 2;
  }
}

#elif FUNC == 2
// use `unsigned int` to reduce one or two instructions
void Func(int a[], int &r) {
  unsigned int i;
  for (i = 0; i < 100; i++) {
    a[i] = r + i / 2;
  }
}

#elif FUNC == 3
void Func(int a[], int &r) {
  unsigned int i;
  // tell the compiler no pointer alias for `r` so that the 'r' value could be
  // saved in a register instead of fetching from memory.
  int induction = r;
  for (i = 0; i < 100; i++) {
    a[i] = induction + i / 2;
  }
}

#else
// use of induction variable:
//
//   An expression that is a linear function of a loop counter can be calculated
//   by adding a constant to the previous value
//
void Func(int a[], int &r) {
  unsigned int i;
  int induction = r;
  for (i = 0; i < 100; i+=2) {
    a[i] = induction;
    a[i+1] = induction;
    induction++;
  }
}
#endif
