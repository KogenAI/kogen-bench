use tally::agg::Aggregator;
#[test]fn overflow_is_checked(){let mut a=Aggregator::default();assert!(a.add_count("x",u64::MAX).is_ok());assert!(a.add_count("x",1).is_err());assert_eq!(a.count("x"),u64::MAX);}
