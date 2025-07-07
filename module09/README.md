# Module 9 - Graph Queries

In this module you will:

- Run graph queries
- Explore a graph query plan

## Run graph queries 

Run this simple graph query that returns a single node.

```sql
graph network
match (r:Router {router_id: "core1"})
return r.description
```

Click on `EXPLANATION` to check the query  plan.

In this case the query plan is pretty simple. It reads a single table and the execution is performed within a single split.

Run the following graph query that returns the routers connected to a certain node.

```sql
graph network
match (:Router {router_id: "core1"})-[:Connected]-(neighbour:Router)
return neighbour.router_id
```

In this case the execution plan is significantly more complex. It involves 3 tables and the execution is distributed.


Find the paths between two edge routers and the number of hops for each path.

```sql
graph network
match (:Router {router_id: 'edge1'})-[hops:Connected]-{1,5}(:Router {router_id: 'edge8'})
return ARRAY_LENGTH(hops) as hops
```

Find the top 10 paths between two edge routers that guarantee a minimum capacity of 150, order by minimum capacity descending.

```sql
graph network
match (:Router {router_id: 'edge1'})-[hops:Connected]-{1,5}(:Router {router_id: 'edge8'})
let min_capacity = min(hops.capacity)
filter min_capacity >= 150
return min_capacity
order by min_capacity desc
limit 10
```

**Challenge:** Can you find the top 10 paths with the lowest latency between those two routers?

