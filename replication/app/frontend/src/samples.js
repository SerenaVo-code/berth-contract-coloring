// Sinh tự động bởi tools/make_samples.py từ testcases/, đừng sửa tay.
export const SAMPLES = {
 "berth": [
  {
   "id": "m1-T05",
   "label": "Bốn kết quả khác nhau",
   "input": {
    "ships": [
     {
      "name": "Tàu 1",
      "s": 11.0,
      "e": 19.0
     },
     {
      "name": "Tàu 2",
      "s": 5.5,
      "e": 11.0
     },
     {
      "name": "Tàu 3",
      "s": 1.0,
      "e": 3.5
     },
     {
      "name": "Tàu 4",
      "s": 10.5,
      "e": 12.5
     },
     {
      "name": "Tàu 5",
      "s": 0.5,
      "e": 5.0
     },
     {
      "name": "Tàu 6",
      "s": 0.5,
      "e": 4.0
     },
     {
      "name": "Tàu 7",
      "s": 10.0,
      "e": 14.5
     },
     {
      "name": "Tàu 8",
      "s": 3.0,
      "e": 8.0
     }
    ],
    "pairs": [
     [
      7,
      6
     ],
     [
      6,
      5
     ]
    ],
    "F": 500,
    "r": 40
   }
  },
  {
   "id": "m1-D03",
   "label": "Chu trình lẻ do ràng buộc phụ",
   "input": {
    "ships": [
     {
      "name": "Tàu 1",
      "s": 0,
      "e": 1
     },
     {
      "name": "Tàu 2",
      "s": 0,
      "e": 1
     },
     {
      "name": "Tàu 3",
      "s": 0,
      "e": 1
     },
     {
      "name": "Tàu 4",
      "s": 0,
      "e": 1
     },
     {
      "name": "Tàu 5",
      "s": 0,
      "e": 1
     }
    ],
    "pairs": [
     [
      0,
      1
     ],
     [
      1,
      2
     ],
     [
      2,
      3
     ],
     [
      3,
      4
     ],
     [
      4,
      0
     ]
    ],
    "F": 100,
    "r": 10
   }
  }
 ],
 "assign": [
  {
   "id": "m2-D02",
   "label": "Tham lam bị kẹt",
   "input": {
    "ships": [
     {
      "name": "Tàu 1",
      "s": 7.5,
      "e": 11.0,
      "need": [
       "hóa chất"
      ]
     },
     {
      "name": "Tàu 2",
      "s": 0.5,
      "e": 4.5,
      "need": [
       "hàng lạnh"
      ]
     },
     {
      "name": "Tàu 3",
      "s": 0.0,
      "e": 1.0,
      "need": [
       "hàng lạnh",
       "buộc dây"
      ]
     },
     {
      "name": "Tàu 4",
      "s": 3.5,
      "e": 4.0,
      "need": [
       "cẩu"
      ]
     },
     {
      "name": "Tàu 5",
      "s": 3.5,
      "e": 4.5,
      "need": [
       "hóa chất"
      ]
     },
     {
      "name": "Tàu 6",
      "s": 6.5,
      "e": 9.0,
      "need": [
       "hàng lạnh",
       "buộc dây"
      ]
     }
    ],
    "teams": [
     {
      "name": "Đội 1",
      "skills": [
       "hóa chất",
       "hàng lạnh",
       "cẩu",
       "buộc dây"
      ],
      "rate": 15
     },
     {
      "name": "Đội 2",
      "skills": [
       "buộc dây",
       "hàng lạnh",
       "hóa chất"
      ],
      "rate": 15
     },
     {
      "name": "Đội 3",
      "skills": [
       "hàng lạnh"
      ],
      "rate": 29
     },
     {
      "name": "Đội 4",
      "skills": [
       "hàng lạnh",
       "cẩu"
      ],
      "rate": 36
     }
    ],
    "pairs": [
     [
      2,
      0
     ]
    ]
   }
  },
  {
   "id": "m2-D01",
   "label": "Vô nghiệm (vi phạm Hall)",
   "input": {
    "ships": [
     {
      "name": "S0",
      "s": 0,
      "e": 5,
      "need": [
       "cẩu"
      ]
     },
     {
      "name": "S1",
      "s": 0,
      "e": 5,
      "need": [
       "cẩu"
      ]
     },
     {
      "name": "S2",
      "s": 0,
      "e": 5,
      "need": [
       "cẩu"
      ]
     }
    ],
    "teams": [
     {
      "name": "Đội 1",
      "skills": [
       "cẩu",
       "buộc dây",
       "hàng lạnh",
       "hóa chất"
      ],
      "rate": 10
     },
     {
      "name": "Đội 2",
      "skills": [
       "cẩu",
       "buộc dây",
       "hàng lạnh",
       "hóa chất"
      ],
      "rate": 12
     }
    ],
    "pairs": []
   }
  }
 ],
 "knapsack": [
  {
   "id": "m3-T04",
   "label": "Tham lam sai",
   "input": {
    "items": [
     {
      "name": "A",
      "w": 10,
      "v": 60
     },
     {
      "name": "B",
      "w": 20,
      "v": 100
     },
     {
      "name": "C",
      "w": 30,
      "v": 120
     }
    ],
    "W": 50
   }
  },
  {
   "id": "m3-T01",
   "label": "10 yêu cầu ngẫu nhiên",
   "input": {
    "items": [
     {
      "name": "Yêu cầu 1",
      "w": 1,
      "v": 15
     },
     {
      "name": "Yêu cầu 2",
      "w": 12,
      "v": 12
     },
     {
      "name": "Yêu cầu 3",
      "w": 2,
      "v": 36
     },
     {
      "name": "Yêu cầu 4",
      "w": 10,
      "v": 16
     },
     {
      "name": "Yêu cầu 5",
      "w": 10,
      "v": 33
     },
     {
      "name": "Yêu cầu 6",
      "w": 7,
      "v": 10
     },
     {
      "name": "Yêu cầu 7",
      "w": 7,
      "v": 30
     },
     {
      "name": "Yêu cầu 8",
      "w": 10,
      "v": 5
     },
     {
      "name": "Yêu cầu 9",
      "w": 5,
      "v": 33
     },
     {
      "name": "Yêu cầu 10",
      "w": 9,
      "v": 49
     }
    ],
    "W": 35
   }
  }
 ],
 "binpack": [
  {
   "id": "m4-D02",
   "label": "First-Fit giảm dần không tối ưu",
   "input": {
    "items": [
     {
      "name": "Lô 1",
      "w": 51
     },
     {
      "name": "Lô 2",
      "w": 21
     },
     {
      "name": "Lô 3",
      "w": 29
     },
     {
      "name": "Lô 4",
      "w": 21
     },
     {
      "name": "Lô 5",
      "w": 58
     },
     {
      "name": "Lô 6",
      "w": 36
     },
     {
      "name": "Lô 7",
      "w": 50
     },
     {
      "name": "Lô 8",
      "w": 26
     }
    ],
    "C": 100
   }
  },
  {
   "id": "m4-T04",
   "label": "First-Fit tệ hơn FFD",
   "input": {
    "items": [
     {
      "name": "Lô 1",
      "w": 2
     },
     {
      "name": "Lô 2",
      "w": 5
     },
     {
      "name": "Lô 3",
      "w": 6
     },
     {
      "name": "Lô 4",
      "w": 2
     },
     {
      "name": "Lô 5",
      "w": 5
     },
     {
      "name": "Lô 6",
      "w": 1
     },
     {
      "name": "Lô 7",
      "w": 6
     },
     {
      "name": "Lô 8",
      "w": 7
     },
     {
      "name": "Lô 9",
      "w": 2
     }
    ],
    "C": 10
   }
  }
 ]
}
