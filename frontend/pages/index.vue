<template>
  <div>
    <Navbar />
    <section class="p-10">
      <h1>Velkommen!</h1>
      <p>At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga.</p>

      <h2>Dette er en test...</h2>
      <p>Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>
      <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?</p>
      <ul>
        <li>Listeting 1</li>
        <li>Listeting 2</li>
        <li>Listeting 3</li>
      </ul>
      <p>Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil <a href="#">impedit quo minus id</a> quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.</p>

      <h3>Dette er en test...</h3>
      <p>Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis.</p>

      <a href="#">Dette er en link</a>

      <br><br>

      <blockquote>
        <p>På plassen står en statue av henne i helfigur, utført i bronse av Nic Schiøll og avduket i 1966.</p>
      </blockquote>
    </section>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  
  const enabled = ref(false)
</script>
