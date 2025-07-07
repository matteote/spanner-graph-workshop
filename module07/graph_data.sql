INSERT INTO
  Router (router_id,
    description)
VALUES
  ('core1', 'core router 1'),
  ('core2', 'core router 2'),
  ('core3', 'core router 3'),
  ('core4', 'core router 4'),
  ('core5', 'core router 5'),
  ('edge1', 'edge router 1'),
  ('edge2', 'edge router 2'),
  ('edge3', 'edge router 3'),
  ('edge4', 'edge router 4'),
  ('edge5', 'edge router 5'),
  ('edge6', 'edge router 6'),
  ('edge7', 'edge router 7'),
  ('edge8', 'edge router 8'),
  ('edge9', 'edge router 9'),
  ('edge10', 'edge router 10'),
  ('edge11', 'edge router 11'),
  ('edge12', 'edge router 12'),
  ('edge13', 'edge router 13'),
  ('edge14', 'edge router 14'),
  ('edge15', 'edge router 15'),
  ('edge16', 'edge router 16'),
  ('edge17', 'edge router 17'),
  ('edge18', 'edge router 18'),
  ('edge19', 'edge router 19'),
  ('edge20', 'edge router 20');


INSERT INTO
  Connected (router_id,
    to_router_id,
    `capacity`,
    latency)
VALUES
  ( 'core1', 'core2', 185, 4),
  ( 'core1', 'core3', 152, 4),
  ( 'core1', 'core4', 224, 2),
  ( 'core1', 'core5', 264, 3),
  ( 'core2', 'core3', 110, 4),
  ( 'core2', 'core4', 178, 3),
  ( 'core2', 'core5', 220, 4),
  ( 'core3', 'core4', 113, 2),
  ( 'core3', 'core5', 239, 3),
  ( 'core4', 'core5', 174, 2);

INSERT INTO
  Connected (router_id,
    to_router_id,
    `capacity`,
    latency)
VALUES
  ( 'edge1', 'core1',  225, 10),
  ( 'edge2', 'core2',  123, 14),
  ( 'edge3', 'core3',  151, 11),
  ( 'edge4', 'core4',  206, 9),
  ( 'edge5', 'core5',  112, 12),
  ( 'edge6', 'core1',  163, 11),
  ( 'edge7', 'core2',  255, 14),
  ( 'edge8', 'core3',  200, 15),
  ( 'edge9', 'core4',  114, 14),
  ( 'edge10', 'core5', 282, 9),
  ( 'edge11', 'core1', 220, 10),
  ( 'edge12', 'core2', 129, 5),
  ( 'edge13', 'core3', 125, 6),
  ( 'edge14', 'core4', 184, 6),
  ( 'edge15', 'core5', 106, 6),
  ( 'edge16', 'core1', 198, 5),
  ( 'edge17', 'core2', 205, 5),
  ( 'edge18', 'core3', 230, 15),
  ( 'edge19', 'core4', 285, 6),
  ( 'edge20', 'core5', 146, 13);
